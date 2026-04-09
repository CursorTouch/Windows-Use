from dataclasses import dataclass,field
from typing import TYPE_CHECKING, Optional,Any,Union
import json

WARNING_MESSAGE="The desktop UI services are temporarily unavailable. Please wait a few seconds and continue."
EMPTY_MESSAGE="No elements found"

if TYPE_CHECKING:
    from windows_use.uia.core import Rect

@dataclass
class TreeState:
    status:bool=True
    root_node:Optional['TreeElementNode']=None
    dom_node:Optional['ScrollElementNode']=None
    interactive_nodes:list['TreeElementNode']|None=field(default_factory=list)
    scrollable_nodes:list['ScrollElementNode']|None=field(default_factory=list)
    dom_informative_nodes:list['TextElementNode']|None=field(default_factory=list)

    def interactive_elements_to_string(self) -> str:
        parts = []
        if not self.status:
            parts.append(WARNING_MESSAGE)
            return "\n".join(parts)
        if not self.interactive_nodes and self.status:
            parts.append(EMPTY_MESSAGE)
            return "\n".join(parts)
        # TOON-like format: Pipe-separated values with clear header
        # Using abbreviations in header to save tokens
        header = "# id|window|control_type|name|coords|metadata"
        rows = [header]
        for idx, node in enumerate(self.interactive_nodes):
            row = f"{idx}|{node.window_name}|{node.control_type}|{node.name}|{node.center.to_string()}|{json.dumps(node.metadata)}"
            rows.append(row)
        parts.append("\n".join(rows))
        return "\n".join(parts)

    def build_selector_map(self) -> 'SelectorMap':
        """Build a SelectorMap from all interactive and scrollable nodes in this tree state."""
        nodes: list = list(self.interactive_nodes or []) + list(self.scrollable_nodes or [])
        return SelectorMap(nodes)

    def scrollable_elements_to_string(self) -> str:
        parts = []
        if not self.status:
            parts.append(WARNING_MESSAGE)
            return "\n".join(parts)
        if not self.scrollable_nodes and self.status:
            parts.append(EMPTY_MESSAGE)
            return "\n".join(parts)
        # TOON-like format
        header = "# id|window|control_type|name|coords|metadata"
        rows = [header]
        base_index = len(self.interactive_nodes)
        for idx, node in enumerate(self.scrollable_nodes):
            row = (f"{base_index + idx}|{node.window_name}|{node.control_type}|{node.name}|"
                   f"{node.center.to_string()}|{json.dumps(node.metadata)}")
            rows.append(row)
        parts.append("\n".join(rows))
        return "\n".join(parts)
    
@dataclass
class BoundingBox:
    left:int
    top:int
    right:int
    bottom:int
    width:int
    height:int

    @classmethod
    def from_bounding_rectangle(cls,bounding_rectangle:'Rect')->'BoundingBox':
        return cls(
            left=bounding_rectangle.left,
            top=bounding_rectangle.top,
            right=bounding_rectangle.right,
            bottom=bounding_rectangle.bottom,
            width=bounding_rectangle.width(),
            height=bounding_rectangle.height()
        )

    def get_center(self)->'Center':
        return Center(x=self.left+self.width//2,y=self.top+self.height//2)

    def xywh_to_string(self):
        return f'({self.left},{self.top},{self.width},{self.height})'
    
    def xyxy_to_string(self):
        x1,y1,x2,y2=self.convert_xywh_to_xyxy()
        return f'({x1},{y1},{x2},{y2})'
    
    def convert_xywh_to_xyxy(self)->tuple[int,int,int,int]:
        x1,y1=self.left,self.top
        x2,y2=self.left+self.width,self.top+self.height
        return x1,y1,x2,y2

@dataclass
class Center:
    x:int
    y:int

    def to_string(self)->str:
        return f'({self.x},{self.y})'

@dataclass
class TreeElementNode:
    bounding_box: BoundingBox
    center: Center
    name: str=''
    control_type: str=''
    window_name: str=''
    xpath: str=''
    hwnd: int=0
    metadata:dict[str,Any]=field(default_factory=dict)

    def update_from_node(self,node:'TreeElementNode'):
        self.name=node.name
        self.control_type=node.control_type
        self.window_name=node.window_name
        self.value=node.value
        self.shortcut=node.shortcut
        self.bounding_box=node.bounding_box
        self.center=node.center
        self.metadata=node.metadata

    # Legacy method kept for compatibility if needed, but not used in new format
    def to_row(self, index: int):
        return [index, self.window_name, self.control_type, self.name, self.value, self.shortcut, self.center.to_string(),self.is_focused]

@dataclass
class ScrollElementNode:
    name: str
    control_type: str
    window_name: str
    bounding_box: BoundingBox
    center: Center
    xpath: str=''
    hwnd: int=0
    metadata:dict[str,Any]=field(default_factory=dict)

    # Legacy method kept for compatibility
    def to_row(self, index: int, base_index: int):
        return [
            base_index + index,
            self.window_name,
            self.control_type,
            self.name,
            self.center.to_string(),
            json.dumps(self.metadata)
        ]

@dataclass
class TextElementNode:
    text:str

ElementNode=TreeElementNode|ScrollElementNode|TextElementNode

_SelectorNode = Union[TreeElementNode, ScrollElementNode]

class SelectorMap:
    """Maps element labels to their TreeElementNodes for cursor-free element lookup.

    Provides fast access to interactive and scrollable elements by name,
    with optional control_type filtering for disambiguation when multiple
    elements share the same label.

    Usage:
        selector = tree_state.build_selector_map()

        # Exact label lookup
        node = selector['Submit']           # first element named 'Submit'
        node = selector.get('Submit')       # same, returns None if not found
        node = selector.get('OK', control_type='ButtonControl')  # disambiguate

        # All matches for a label
        nodes = selector.get_all('File')    # e.g. File menu + File tab

        # Partial / case-insensitive search
        nodes = selector.find('save')       # finds 'Save', 'Save As', 'Autosave'

        # Resolve to live UIA element (cursor-free)
        element = desktop.get_element_from_window_xpath(node.hwnd, node.xpath)
    """

    def __init__(self, nodes: list[_SelectorNode]):
        # name → all nodes with that name (preserves insertion order)
        self._by_name: dict[str, list[_SelectorNode]] = {}
        # (name, control_type) → nodes, for disambiguation
        self._by_label_type: dict[tuple[str, str], list[_SelectorNode]] = {}

        for node in nodes:
            name = (node.name or '').strip()
            if not name:
                continue
            ct = node.control_type
            self._by_name.setdefault(name, []).append(node)
            self._by_label_type.setdefault((name, ct), []).append(node)

    def get(self, label: str, control_type: str | None = None) -> _SelectorNode | None:
        """Return the first element matching label, optionally filtered by control_type."""
        if control_type:
            nodes = self._by_label_type.get((label, control_type), [])
        else:
            nodes = self._by_name.get(label, [])
        return nodes[0] if nodes else None

    def get_all(self, label: str, control_type: str | None = None) -> list[_SelectorNode]:
        """Return all elements matching label, optionally filtered by control_type."""
        if control_type:
            return list(self._by_label_type.get((label, control_type), []))
        return list(self._by_name.get(label, []))

    def find(self, label: str) -> list[_SelectorNode]:
        """Case-insensitive partial label match. Useful when exact name is unknown."""
        label_lower = label.lower()
        results = []
        for name, nodes in self._by_name.items():
            if label_lower in name.lower():
                results.extend(nodes)
        return results

    def xpath_of(self, label: str, control_type: str | None = None) -> str | None:
        """Shortcut: return xpath of first matching element, or None."""
        node = self.get(label, control_type)
        return node.xpath if node else None

    def hwnd_of(self, label: str, control_type: str | None = None) -> int | None:
        """Shortcut: return hwnd of first matching element, or None."""
        node = self.get(label, control_type)
        return node.hwnd if node else None

    def __getitem__(self, label: str) -> _SelectorNode:
        node = self.get(label)
        if node is None:
            raise KeyError(f'No element with label {label!r}')
        return node

    def __contains__(self, label: str) -> bool:
        return label in self._by_name

    def __len__(self) -> int:
        return sum(len(v) for v in self._by_name.values())

    def keys(self) -> list[str]:
        return list(self._by_name.keys())

    def __repr__(self) -> str:
        return f'SelectorMap({len(self._by_name)} labels, {len(self)} elements)'
