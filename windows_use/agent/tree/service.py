from windows_use.agent.tree.config import INTERACTIVE_CONTROL_TYPE_NAMES,DOCUMENT_CONTROL_TYPE_NAMES,INFORMATIVE_CONTROL_TYPE_NAMES, DEFAULT_ACTIONS, INTERACTIVE_ROLES, THREAD_MAX_RETRIES
from windows_use.uia import Control,ImageControl,ScrollPattern,WindowControl,Rect,GetRootControl,PatternId,AccessibleRoleNames,PaneControl,GroupControl,StructureChangeType
from windows_use.agent.tree.views import TreeElementNode, ScrollElementNode, TextElementNode, Center, BoundingBox, TreeState
from windows_use.agent.tree.utils import random_point_within_bounding_box
from concurrent.futures import ThreadPoolExecutor, as_completed
from windows_use.agent.desktop.views import App
from PIL import Image, ImageFont, ImageDraw
from typing import TYPE_CHECKING,Optional
from time import sleep
import logging
import random
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

if TYPE_CHECKING:
    from windows_use.agent.desktop.service import Desktop
    
class Tree:
    def __init__(self,desktop:'Desktop'):
        self.desktop=desktop
        self.screen_size=desktop.get_screen_size()
        self.dom:Optional[Control]=None
        self.dom_bounding_box:BoundingBox=None
        self.screen_box=BoundingBox(
            top=0, left=0, bottom=self.screen_size.height, right=self.screen_size.width,
            width=self.screen_size.width, height=self.screen_size.height
        )
        self.tree_state=None
        self._last_structure_event = None

    def get_state(self,active_app:App,other_apps:list[App])->TreeState:
        root=GetRootControl()
        other_apps_handle=set(map(lambda other_app: other_app.handle,other_apps))
        apps=list(filter(lambda app:(app.NativeWindowHandle not in other_apps_handle) and not self.desktop.is_overlay_app(app),root.GetChildren()))
        del other_apps_handle
        if active_app:
            apps=list(filter(lambda app:app.ClassName!='Progman',apps))
        interactive_nodes,scrollable_nodes,dom_informative_nodes=self.get_appwise_nodes(apps=apps)
        root_node=TreeElementNode(
            name="Desktop",
            runtime_id=(),
            cursor_type="",
            control_type="PaneControl",
            bounding_box=self.screen_box,
            center=self.screen_box.get_center(),
            app_name="Desktop",
            xpath='',
            value='',
            shortcut='',
            is_focused=False
        )
        if self.dom:
            scroll_pattern:ScrollPattern=self.dom.GetPattern(PatternId.ScrollPattern)
            dom_node=ScrollElementNode(
                name="DOM",
                runtime_id=(),
                control_type="DocumentControl",
                bounding_box=self.dom_bounding_box,
                center=self.dom_bounding_box.get_center(),
                horizontal_scrollable=scroll_pattern.HorizontallyScrollable if scroll_pattern else False,
                horizontal_scroll_percent=scroll_pattern.HorizontalScrollPercent if scroll_pattern and scroll_pattern.HorizontallyScrollable else 0,
                vertical_scrollable=scroll_pattern.VerticallyScrollable if scroll_pattern else False,
                vertical_scroll_percent=scroll_pattern.VerticalScrollPercent if scroll_pattern and scroll_pattern.VerticallyScrollable else 0,
                xpath='',
                app_name="DOM",
                is_focused=False
            )
        else:
            dom_node=None
        self.tree_state=TreeState(root_node=root_node,dom_node=dom_node,interactive_nodes=interactive_nodes,scrollable_nodes=scrollable_nodes,dom_informative_nodes=dom_informative_nodes)
        return self.tree_state

    def get_appwise_nodes(self,apps:list[Control]) -> tuple[list[TreeElementNode],list[ScrollElementNode],list[TextElementNode]]:
        interactive_nodes, scrollable_nodes, dom_informative_nodes = [], [], []
        with ThreadPoolExecutor() as executor:
            retry_counts = {app: 0 for app in apps}
            future_to_app = {
                executor.submit(
                    self.get_nodes, app, 
                    self.desktop.is_app_browser(app)
                ): app
                for app in apps
            }
            while future_to_app:  # keep running until no pending futures
                for future in as_completed(list(future_to_app)):
                    app = future_to_app.pop(future)  # remove completed future
                    try:
                        result = future.result()
                        if result:
                            element_nodes, scroll_nodes, dom_informative_nodes = result
                            interactive_nodes.extend(element_nodes)
                            scrollable_nodes.extend(scroll_nodes)
                            dom_informative_nodes.extend(dom_informative_nodes)
                    except Exception as e:
                        retry_counts[app] += 1
                        logger.debug(f"Error in processing node {app.Name}, retry attempt {retry_counts[app]}\nError: {e}")
                        if retry_counts[app] < THREAD_MAX_RETRIES:
                            new_future = executor.submit(self.get_nodes, app, self.desktop.is_app_browser(app))
                            future_to_app[new_future] = app
                        else:
                            logger.error(f"Task failed completely for {app.Name} after {THREAD_MAX_RETRIES} retries")
        return interactive_nodes,scrollable_nodes,dom_informative_nodes
    
    def iou_bounding_box(self,window_box: Rect,element_box: Rect,) -> BoundingBox:
        # Step 1: Intersection of element and window (existing logic)
        intersection_left = max(window_box.left, element_box.left)
        intersection_top = max(window_box.top, element_box.top)
        intersection_right = min(window_box.right, element_box.right)
        intersection_bottom = min(window_box.bottom, element_box.bottom)

        # Step 2: Clamp to screen boundaries (new addition)
        intersection_left = max(self.screen_box.left, intersection_left)
        intersection_top = max(self.screen_box.top, intersection_top)
        intersection_right = min(self.screen_box.right, intersection_right)
        intersection_bottom = min(self.screen_box.bottom, intersection_bottom)

        # Step 3: Validate intersection
        if (intersection_right > intersection_left and intersection_bottom > intersection_top):
            bounding_box = BoundingBox(
                left=intersection_left,
                top=intersection_top,
                right=intersection_right,
                bottom=intersection_bottom,
                width=intersection_right - intersection_left,
                height=intersection_bottom - intersection_top
            )
        else:
            # No valid visible intersection (either outside window or screen)
            bounding_box = BoundingBox(
                left=0,
                top=0,
                right=0,
                bottom=0,
                width=0,
                height=0
            )
        return bounding_box

    def is_element_visible(self, node:Control, threshold:int=0):
        is_control=node.IsControlElement
        box=node.BoundingRectangle
        if box.isempty():
            return False
        width=box.width()
        height=box.height()
        area=width*height
        is_offscreen=(not node.IsOffscreen) or node.ControlTypeName in ['EditControl']
        return area > threshold and is_offscreen and is_control
    
    def is_element_enabled(self, node: Control):
        try:
            return node.IsEnabled
        except Exception:
            return False
        
    def is_element_role_interactive(self, node: Control):
        legacy_pattern=node.GetLegacyIAccessiblePattern()
        try:
            return AccessibleRoleNames.get(legacy_pattern.Role, "Default") in INTERACTIVE_ROLES
        except Exception:
            return False
            
    def is_default_action(self, node:Control):
        legacy_pattern=node.GetLegacyIAccessiblePattern()
        default_action=legacy_pattern.DefaultAction.title()
        if default_action in DEFAULT_ACTIONS:
            return True
        return False
        
    def is_element_image(self, node:Control):
        if isinstance(node,ImageControl):
            if node.LocalizedControlType=='graphic' or not node.IsKeyboardFocusable:
                return True
        return False
        
    def is_element_text(self, node:Control):
        try:
            if node.ControlTypeName in INFORMATIVE_CONTROL_TYPE_NAMES:
                if self.is_element_visible(node) and self.is_element_enabled(node) and not self.is_element_image(node):
                    return True
        except Exception:
            return False
        return False
            
    def is_window_modal(self, node:WindowControl):
        try:
            window_pattern=node.GetWindowPattern()
            return window_pattern.IsModal
        except Exception:
            return False
            
    def is_keyboard_focusable(self, node:Control):
        try:
            if node.ControlTypeName in set(['EditControl','ButtonControl','CheckBoxControl','RadioButtonControl','TabItemControl']):
                return True
            return node.IsKeyboardFocusable
        except Exception:
            return False
            
    def element_has_child_element(self, node:Control,control_type:str,child_control_type:str):
        if node.LocalizedControlType==control_type:
            first_child=node.GetFirstChildControl()
            if first_child is None:
                return False
            return first_child.LocalizedControlType==child_control_type
            
    def group_has_no_name(self, node:Control):
        try:
            if node.ControlTypeName=='GroupControl':
                if not node.Name.strip():
                    return True
            return False
        except Exception:
            return False
            
    def is_element_scrollable(self, node:Control):
        try:
            if (node.ControlTypeName in INTERACTIVE_CONTROL_TYPE_NAMES|INFORMATIVE_CONTROL_TYPE_NAMES) or node.IsOffscreen:
                return False
            scroll_pattern:ScrollPattern=node.GetPattern(PatternId.ScrollPattern)
            if scroll_pattern is None:
                return False
            return scroll_pattern.VerticallyScrollable
        except Exception:
            return False
            
    def is_element_interactive(self, node:Control, is_browser:bool):
        try:
            if is_browser and node.ControlTypeName in set(['DataItemControl','ListItemControl']) and not self.is_keyboard_focusable(node):
                return False
            elif not is_browser and node.ControlTypeName=="ImageControl" and self.is_keyboard_focusable(node):
                return True
            elif node.ControlTypeName in INTERACTIVE_CONTROL_TYPE_NAMES|DOCUMENT_CONTROL_TYPE_NAMES:
                return self.is_element_visible(node) and self.is_element_enabled(node) and self.is_element_role_interactive(node) and (not self.is_element_image(node) or self.is_keyboard_focusable(node))
            elif node.ControlTypeName=='GroupControl':
                if is_browser:
                    return self.is_element_visible(node) and self.is_element_enabled(node) and self.is_element_role_interactive(node) and (self.is_default_action(node) or self.is_keyboard_focusable(node))
                    # else:
                    #     return is_element_visible(node) and is_element_enabled(node) and is_default_action(node)
        except Exception:
            return False
        return False

    def _dom_correction(self, node:Control, dom_interactive_nodes:list[TreeElementNode], app_name:str):
        if self.element_has_child_element(node,'list item','link') or self.element_has_child_element(node,'item','link'):
            dom_interactive_nodes.pop()
            return None
        elif node.ControlTypeName=='GroupControl':
            dom_interactive_nodes.pop()
            if self.is_keyboard_focusable(node):
                child=node
                try:
                    while child.GetFirstChildControl() is not None:
                        if child.ControlTypeName in INTERACTIVE_CONTROL_TYPE_NAMES:
                            return None
                        child=child.GetFirstChildControl()
                except Exception:
                    return None
                if child.ControlTypeName!='TextControl':
                    return None
                runtime_id=node.GetRuntimeId()
                legacy_pattern=node.GetLegacyIAccessiblePattern()
                value=legacy_pattern.Value
                element_bounding_box = node.BoundingRectangle
                bounding_box=self.iou_bounding_box(self.dom_bounding_box,element_bounding_box)
                center = bounding_box.get_center()
                is_focused=node.HasKeyboardFocus
                dom_interactive_nodes.append(TreeElementNode(**{
                    'name':child.Name.strip(),
                    'runtime_id':tuple(runtime_id),
                    'cursor_type':'',
                    'control_type':node.LocalizedControlType,
                    'value':value,
                    'shortcut':node.AcceleratorKey,
                    'bounding_box':bounding_box,
                    'xpath':'',
                    'center':center,
                    'app_name':app_name,
                    'is_focused':is_focused
                }))
        elif self.element_has_child_element(node,'link','heading'):
            dom_interactive_nodes.pop()
            node=node.GetFirstChildControl()
            control_type='link'
            runtime_id=node.GetRuntimeId()
            legacy_pattern=node.GetLegacyIAccessiblePattern()
            value=legacy_pattern.Value
            element_bounding_box = node.BoundingRectangle
            bounding_box=self.iou_bounding_box(self.dom_bounding_box,element_bounding_box)
            center = bounding_box.get_center()
            is_focused=node.HasKeyboardFocus
            dom_interactive_nodes.append(TreeElementNode(**{
                'name':node.Name.strip(),
                'runtime_id':tuple(runtime_id),
                'cursor_type':'',
                'control_type':control_type,
                'value':node.Name.strip(),
                'shortcut':node.AcceleratorKey,
                'bounding_box':bounding_box,
                'xpath':'',
                'center':center,
                'app_name':app_name,
                'is_focused':is_focused
            }))

    def tree_traversal(self, node: Control, window_bounding_box:Rect, app_name:str, is_browser:bool, 
                    interactive_nodes:Optional[list[TreeElementNode]]=None, scrollable_nodes:Optional[list[ScrollElementNode]]=None, 
                    dom_interactive_nodes:Optional[list[TreeElementNode]]=None, dom_informative_nodes:Optional[list[TextElementNode]]=None,
                    is_dom:bool=False, is_dialog:bool=False):
        # Checks to skip the nodes that are not interactive
        if node.IsOffscreen and (node.ControlTypeName not in set(["GroupControl","EditControl","TitleBarControl"])) and node.ClassName not in set(["Popup","Windows.UI.Core.CoreComponentInputSource"]):
            return None
        
        if scrollable_nodes is not None and self.is_element_scrollable(node):
            scroll_pattern:ScrollPattern=node.GetPattern(PatternId.ScrollPattern)
            runtime_id=node.GetRuntimeId()
            box = node.BoundingRectangle
            # Get the center
            x,y=random_point_within_bounding_box(node=node,scale_factor=0.8)
            center = Center(x=x,y=y)
            scrollable_nodes.append(ScrollElementNode(**{
                'name':node.Name.strip() or node.AutomationId or node.LocalizedControlType.capitalize() or "''",
                'runtime_id':tuple(runtime_id),
                'control_type':node.LocalizedControlType.title(),
                'bounding_box':BoundingBox(**{
                    'left':box.left,
                    'top':box.top,
                    'right':box.right,
                    'bottom':box.bottom,
                    'width':box.width(),
                    'height':box.height()
                }),
                'center':center,
                'xpath':'',
                'horizontal_scrollable':scroll_pattern.HorizontallyScrollable,
                'horizontal_scroll_percent':scroll_pattern.HorizontalScrollPercent if scroll_pattern.HorizontallyScrollable else 0,
                'vertical_scrollable':scroll_pattern.VerticallyScrollable,
                'vertical_scroll_percent':scroll_pattern.VerticalScrollPercent if scroll_pattern.VerticallyScrollable else 0,
                'app_name':app_name,
                'is_focused':node.HasKeyboardFocus
            }))
                
        if interactive_nodes is not None and self.is_element_interactive(node, is_browser):
            legacy_pattern=node.GetLegacyIAccessiblePattern()
            value=legacy_pattern.Value.strip() if legacy_pattern.Value is not None else ""
            cursor_type=AccessibleRoleNames.get(legacy_pattern.Role, "Default")
            runtime_id=node.GetRuntimeId()
            is_focused=node.HasKeyboardFocus
            name=node.Name.strip()
            element_bounding_box = node.BoundingRectangle
            if is_browser and is_dom:
                bounding_box=self.iou_bounding_box(self.dom_bounding_box,element_bounding_box)
                center = bounding_box.get_center()
                tree_node=TreeElementNode(**{
                    'name':name,
                    'runtime_id':tuple(runtime_id),
                    'control_type':node.LocalizedControlType.title(),
                    'value':value,
                    'shortcut':node.AcceleratorKey,
                    'bounding_box':bounding_box,
                    'center':center,
                    'xpath':'',
                    'app_name':app_name,
                    'is_focused':is_focused
                })
                dom_interactive_nodes.append(tree_node)
                self._dom_correction(node, dom_interactive_nodes, app_name)
            else:
                bounding_box=self.iou_bounding_box(window_bounding_box,element_bounding_box)
                center = bounding_box.get_center()
                tree_node=TreeElementNode(**{
                    'name':name,
                    'runtime_id':tuple(runtime_id),
                    'cursor_type':cursor_type.title(),
                    'control_type':node.LocalizedControlType.title(),
                    'value':value,
                    'shortcut':node.AcceleratorKey,
                    'bounding_box':bounding_box,
                    'center':center,
                    'xpath':'',
                    'app_name':app_name,
                    'is_focused':is_focused
                })
                interactive_nodes.append(tree_node)
        if dom_informative_nodes is not None and self.is_element_text(node):
            if is_browser and is_dom:
                dom_informative_nodes.append(TextElementNode(
                    text=node.Name.strip(),
                ))
        children=node.GetChildren()

        # Recursively traverse the tree the right to left for normal apps and for DOM traverse from left to right
        for child in (children if is_dom else children[::-1]):
            # Incrementally building the xpath
            
            # Check if the child is a DOM element
            if is_browser and child.AutomationId=="RootWebArea":
                bounding_box=child.BoundingRectangle
                self.dom_bounding_box=BoundingBox(left=bounding_box.left,top=bounding_box.top,
                right=bounding_box.right,bottom=bounding_box.bottom,width=bounding_box.width(),
                height=bounding_box.height())
                self.dom=child
                # enter DOM subtree
                self.tree_traversal(child, window_bounding_box, app_name, is_browser, interactive_nodes, scrollable_nodes, dom_interactive_nodes, dom_informative_nodes, is_dom=True, is_dialog=is_dialog)
            # Check if the child is a dialog
            elif isinstance(child,WindowControl):
                if not child.IsOffscreen:
                    if is_dom:
                        bounding_box=child.BoundingRectangle
                        if bounding_box.width() > 0.8*self.dom_bounding_box.width:
                            # Because this window element covers the majority of the screen
                            dom_interactive_nodes.clear()
                    else:
                        if self.is_window_modal(child):
                            # Because this window element is modal
                            interactive_nodes.clear()
                # enter dialog subtree
                self.tree_traversal(child, window_bounding_box, app_name, is_browser, interactive_nodes, scrollable_nodes, dom_interactive_nodes, dom_informative_nodes, is_dom=is_dom, is_dialog=True)
            else:
                # normal non-dialog children
                self.tree_traversal(child, window_bounding_box, app_name, is_browser, interactive_nodes, scrollable_nodes, dom_interactive_nodes, dom_informative_nodes, is_dom=is_dom, is_dialog=is_dialog)

    def app_name_correction(self,app_name:str)->str:
        match app_name:
            case "Progman":
                return "Desktop"
            case 'Shell_TrayWnd'|'Shell_SecondaryTrayWnd':
                return "Taskbar"
            case 'Microsoft.UI.Content.PopupWindowSiteBridge':
                return "Context Menu"
            case _:
                return app_name
    
    def get_nodes(self, node: Control, is_browser:bool=False) -> tuple[list[TreeElementNode],list[ScrollElementNode],list[TextElementNode]]:
        window_bounding_box=node.BoundingRectangle
        
        interactive_nodes, dom_interactive_nodes, dom_informative_nodes, scrollable_nodes = [], [], [], []
        app_name=node.Name.strip()
        app_name=self.app_name_correction(app_name)

        self.tree_traversal(node, window_bounding_box, app_name, is_browser, interactive_nodes, scrollable_nodes, dom_interactive_nodes, dom_informative_nodes, is_dom=False, is_dialog=False)
        logger.debug(f'App name:{app_name}')
        logger.debug(f'Interactive nodes:{len(interactive_nodes)}')
        if is_browser:
            logger.debug(f'DOM interactive nodes:{len(dom_interactive_nodes)}')
            logger.debug(f'DOM informative nodes:{len(dom_informative_nodes)}')
        logger.debug(f'Scrollable nodes:{len(scrollable_nodes)}')

        interactive_nodes.extend(dom_interactive_nodes)
        return (interactive_nodes,scrollable_nodes,dom_informative_nodes)

    def _on_focus_change(self, sender:'ctypes.POINTER(IUIAutomationElement)'):
        """Handle focus change events."""
        # Debounce duplicate events
        current_time = time.time()
        element = Control.CreateControlFromElement(sender)
        runtime_id=element.GetRuntimeId()
        event_key = tuple(runtime_id)
        if hasattr(self, '_last_focus_event') and self._last_focus_event:
            last_key, last_time = self._last_focus_event
            if last_key == event_key and (current_time - last_time) < 1.0:
                return None
        self._last_focus_event = (event_key, current_time)

        try:
            logger.debug(f"[WatchDog] Focus changed to: '{element.Name}' ({element.ControlTypeName})")
        except Exception:
            pass

    def _on_structure_change(self, sender:'ctypes.POINTER(IUIAutomationElement)', changeType:int, runtime_id:list[int]):
        """Handle structure change events."""
        try:
            # Debounce duplicate events
            current_time = time.time()
            event_key = (changeType, tuple(runtime_id))
            if hasattr(self, '_last_structure_event') and self._last_structure_event:
                last_key, last_time = self._last_structure_event
                if last_key == event_key and (current_time - last_time) < 5.0:
                    return None
            self._last_structure_event = (event_key, current_time)

            node = Control.CreateControlFromElement(sender)

            match StructureChangeType(changeType):
                case StructureChangeType.StructureChangeType_ChildAdded|StructureChangeType.StructureChangeType_ChildrenBulkAdded:
                    interactive_nodes=[]
                    app=self.desktop.get_app_from_element(node)
                    app_name=self.app_name_correction(app.name if app else node.Name.strip())
                    is_browser=app.is_browser if app else False
                    if isinstance(node,WindowControl|PaneControl):
                        #Subtree traversal
                        window_bounding_box=app.bounding_box if app else node.BoundingRectangle
                        self.tree_traversal(node,window_bounding_box,app_name,is_browser,interactive_nodes=interactive_nodes)
                    else:
                        #If element is interactive take it else skip it
                        if not self.is_element_interactive(node=node,is_browser=is_browser):
                            return None
                        legacy_pattern=node.GetLegacyIAccessiblePattern()
                        value=legacy_pattern.Value.strip() if legacy_pattern.Value is not None else ""
                        cursor_type=AccessibleRoleNames.get(legacy_pattern.Role, "Default")
                        runtime_id=node.GetRuntimeId()
                        is_focused=node.HasKeyboardFocus
                        name=node.Name.strip()
                        element_bounding_box = node.BoundingRectangle
                        bounding_box=self.iou_bounding_box(window_bounding_box,element_bounding_box)
                        center = bounding_box.get_center()

                        interactive_nodes.append(TreeElementNode(
                            name=name,
                            control_type=cursor_type,
                            bounding_box=bounding_box,
                            center=center,
                            runtime_id=runtime_id,
                            app_name=app_name,
                            value=value,
                            shortcut="",
                            xpath="",
                            is_focused=is_focused
                        ))
                    if self.tree_state:    
                        existing_ids={n.runtime_id for n in self.tree_state.interactive_nodes}
                        interactive_nodes=[n for n in interactive_nodes if n.runtime_id not in existing_ids]
                        self.tree_state.interactive_nodes.extend(interactive_nodes)
                case StructureChangeType.StructureChangeType_ChildrenBulkRemoved | StructureChangeType.StructureChangeType_ChildRemoved:
                    if changeType == StructureChangeType.StructureChangeType_ChildRemoved and self.tree_state:
                        if isinstance(node,WindowControl|PaneControl):
                            parent_bounding_box=BoundingBox.from_bounding_rectangle(node.BoundingRectangle)
                            # Remove nodes spatially contained in the parent (heuristic for "is descendant")
                            def is_contained(n:'TreeElementNode'):
                                cx, cy = n.center.x, n.center.y
                                return (parent_bounding_box.left <= cx <= parent_bounding_box.right and 
                                        parent_bounding_box.top <= cy <= parent_bounding_box.bottom)
                            self.tree_state.interactive_nodes = list(filter(lambda n:not is_contained(n),self.tree_state.interactive_nodes))
                        else:
                            target_runtime_id = tuple(runtime_id)
                            self.tree_state.interactive_nodes = list(filter(lambda n:n.runtime_id != target_runtime_id,self.tree_state.interactive_nodes))
                case StructureChangeType.StructureChangeType_ChildrenInvalidated:
                    #Rebuild subtree
                    parent_bounding_box=BoundingBox.from_bounding_rectangle(node.BoundingRectangle)
                    app=self.desktop.get_app_from_element(node)
                    app_name=self.app_name_correction(app.name if app else node.Name.strip())
                    is_browser=app.is_browser if app else False
                    window_bounding_box=app.bounding_box if app else parent_bounding_box
                    interactive_nodes=[]
                    self.tree_traversal(node,window_bounding_box,app_name,is_browser,interactive_nodes=interactive_nodes)

                    # Remove nodes spatially contained in the parent (heuristic for "is descendant")
                    def is_contained(n:'TreeElementNode'):
                        cx, cy = n.center.x, n.center.y
                        return (parent_bounding_box.left <= cx <= parent_bounding_box.right and 
                                parent_bounding_box.top <= cy <= parent_bounding_box.bottom)
                    
                    if self.tree_state:
                        self.tree_state.interactive_nodes = list(filter(lambda n:not is_contained(n),self.tree_state.interactive_nodes))
                        self.tree_state.interactive_nodes.extend(interactive_nodes)
                case StructureChangeType.StructureChangeType_ChildrenReordered:
                    app=self.desktop.get_app_from_element(node)
                    app_name=self.app_name_correction(app.name if app else node.Name.strip())
                    is_browser=app.is_browser if app else False
                    window_bounding_box=app.bounding_box if app else node.BoundingRectangle
                    interactive_nodes=[]
                    self.tree_traversal(node,window_bounding_box,app_name,is_browser,interactive_nodes=interactive_nodes)
                    
                    # Update existing nodes
                    fresh_nodes_map = {n.runtime_id: n for n in interactive_nodes}
                    def update_node(existing_node:'TreeElementNode'):
                        if new_node:=fresh_nodes_map.get(existing_node.runtime_id):
                            existing_node.update_from_node(new_node)
                    list(map(update_node,self.tree_state.interactive_nodes))
        except Exception as e:
            logger.debug(f"[WatchDog] Structure changed with error: {e}, StructureChangeType={StructureChangeType(changeType).name}")
        
        try:
            logger.debug(f"[WatchDog] Structure changed: Type={StructureChangeType(changeType).name} RuntimeID={tuple(runtime_id)} Sender: '{node.Name}' ({node.ControlTypeName})")
        except Exception:
            pass

    def _on_property_change(self, sender:'ctypes.POINTER(IUIAutomationElement)', propertyId:int, newValue):
        """Handle property change events."""
        try:
            element = Control.CreateControlFromElement(sender)
            logger.debug(f"[WatchDog] Property changed: ID={propertyId} Value={newValue} Element: '{element.Name}' ({element.ControlTypeName})")
        except Exception:
            pass