from dataclasses import dataclass,field
from tabulate import tabulate

@dataclass
class TreeState:
    interactive_nodes:list['TreeElementNode']=field(default_factory=list)
    scrollable_nodes:list['ScrollElementNode']=field(default_factory=list)

    def interactive_elements_to_string(self) -> str:
        if not self.interactive_nodes:
            return "No interactive elements"
        headers = ["Label", "App Name", "ControlType", "Name", "Value", "Shortcut", "Coordinates"]
        rows = [node.to_row(idx) for idx, node in enumerate(self.interactive_nodes)]
        return tabulate(rows, headers=headers, tablefmt="simple")

    def scrollable_elements_to_string(self) -> str:
        if not self.scrollable_nodes:
            return "No scrollable elements"
        headers = [
            "Label", "App Name", "ControlType", "Name", "Coordinates",
            "Horizontal Scrollable", "Horizontal Scroll Percent(%)", "Vertical Scrollable", "Vertical Scroll Percent(%)", "IsFocused"
        ]
        base_index = len(self.interactive_nodes)
        rows = [node.to_row(idx, base_index) for idx, node in enumerate(self.scrollable_nodes)]
        return tabulate(rows, headers=headers, tablefmt="simple")
    
@dataclass
class BoundingBox:
    left:int
    top:int
    right:int
    bottom:int
    width:int
    height:int

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
    name: str
    control_type: str
    value:str
    shortcut: str
    bounding_box: BoundingBox
    center: Center
    xpath:str
    app_name: str

    def to_row(self, index: int):
        return [index, self.app_name, self.control_type, self.name, self.value, self.shortcut, self.center.to_string()]

@dataclass
class ScrollElementNode:
    name: str
    control_type: str
    xpath:str
    app_name: str
    bounding_box: BoundingBox
    center: Center
    horizontal_scrollable: bool
    horizontal_scroll_percent: float
    vertical_scrollable: bool
    vertical_scroll_percent: float
    is_focused: bool

    def to_row(self, index: int, base_index: int):
        return [
            base_index + index,
            self.app_name,
            self.control_type,
            self.name,
            self.center.to_string(),
            self.horizontal_scrollable,
            self.horizontal_scroll_percent,
            self.vertical_scrollable,
            self.vertical_scroll_percent,
            self.is_focused
        ]

ElementNode=TreeElementNode|ScrollElementNode