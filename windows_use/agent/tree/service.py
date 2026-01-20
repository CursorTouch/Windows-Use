from windows_use.agent.tree.config import INTERACTIVE_CONTROL_TYPE_NAMES,DOCUMENT_CONTROL_TYPE_NAMES,INFORMATIVE_CONTROL_TYPE_NAMES, DEFAULT_ACTIONS, INTERACTIVE_ROLES, THREAD_MAX_RETRIES
from windows_use.uia import Control,ImageControl,ScrollPattern,WindowControl,Rect,GetRootControl,PatternId,AccessibleRoleNames,PaneControl,GroupControl,StructureChangeType,TreeScope
from windows_use.agent.tree.views import TreeElementNode, ScrollElementNode, TextElementNode, Center, BoundingBox, TreeState
from windows_use.agent.tree.cache_utils import CacheRequestFactory,CachedPropertyAccessor,CachedControlHelper
from windows_use.agent.tree.utils import random_point_within_bounding_box
from concurrent.futures import ThreadPoolExecutor, as_completed
from windows_use.agent.desktop.views import App
from typing import TYPE_CHECKING,Optional
from time import sleep
import threading
import logging
import random
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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
        # Use thread-local storage for cache requests to prevent threading issues with COM objects
        self._thread_local = threading.local()

    def _get_thread_cache(self):
        """Get or create thread-local cache requests."""
        if not hasattr(self._thread_local, 'element_cache_request'):
            # Initialize cache requests for this thread
            self._thread_local.element_cache_request = CacheRequestFactory.create_tree_traversal_cache()
            self._thread_local.element_cache_request.TreeScope = TreeScope.TreeScope_Element
            
            self._thread_local.children_cache_request = CacheRequestFactory.create_tree_traversal_cache()
            self._thread_local.children_cache_request.TreeScope = TreeScope.TreeScope_Element | TreeScope.TreeScope_Children
            
        return self._thread_local.element_cache_request, self._thread_local.children_cache_request


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



    def element_has_child_element(self, node:Control,control_type:str,child_control_type:str):
        if node.LocalizedControlType==control_type:
            first_child=node.GetFirstChildControl()
            if first_child is None:
                return False
            return first_child.LocalizedControlType==child_control_type

    def _dom_correction(self, node:Control, dom_interactive_nodes:list[TreeElementNode], app_name:str):
        if self.element_has_child_element(node,'list item','link') or self.element_has_child_element(node,'item','link'):
            dom_interactive_nodes.pop()
            return None
        elif node.ControlTypeName=='GroupControl':
            dom_interactive_nodes.pop()
            # Inlined is_keyboard_focusable logic for correction
            control_type_name_check = CachedPropertyAccessor.get_control_type_name(node)
            is_kb_focusable = False
            if control_type_name_check in set(['EditControl','ButtonControl','CheckBoxControl','RadioButtonControl','TabItemControl']):
                 is_kb_focusable = True
            else:
                 is_kb_focusable = CachedPropertyAccessor.get_is_keyboard_focusable(node)

            if is_kb_focusable:
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
                legacy_pattern=node.GetLegacyIAccessiblePattern()
                value=legacy_pattern.Value
                element_bounding_box = node.BoundingRectangle
                bounding_box=self.iou_bounding_box(self.dom_bounding_box,element_bounding_box)
                center = bounding_box.get_center()
                is_focused=node.HasKeyboardFocus
                dom_interactive_nodes.append(TreeElementNode(**{
                    'name':child.Name.strip(),
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
            legacy_pattern=node.GetLegacyIAccessiblePattern()
            value=legacy_pattern.Value
            element_bounding_box = node.BoundingRectangle
            bounding_box=self.iou_bounding_box(self.dom_bounding_box,element_bounding_box)
            center = bounding_box.get_center()
            is_focused=node.HasKeyboardFocus
            dom_interactive_nodes.append(TreeElementNode(**{
                'name':node.Name.strip(),
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
        try:
            # Build cached control if caching is enabled
            if not hasattr(node, '_is_cached'):
                # Use reusable element cache request from thread-local storage
                element_req, _ = self._get_thread_cache()
                node = CachedControlHelper.build_cached_control(node, element_req)
            
            # Checks to skip the nodes that are not interactive
            is_offscreen = CachedPropertyAccessor.get_is_offscreen(node)
            control_type_name = CachedPropertyAccessor.get_control_type_name(node)
            class_name = CachedPropertyAccessor.get_class_name(node)
            
            if is_offscreen and (control_type_name not in set(["GroupControl","EditControl","TitleBarControl"])) and class_name not in set(["Popup","Windows.UI.Core.CoreComponentInputSource"]):
                return None
            
            # Scrollable check
            if scrollable_nodes is not None:
                if (control_type_name not in (INTERACTIVE_CONTROL_TYPE_NAMES|INFORMATIVE_CONTROL_TYPE_NAMES)) and not is_offscreen:
                    try:
                        scroll_pattern:ScrollPattern=node.GetPattern(PatternId.ScrollPattern)
                        if scroll_pattern and scroll_pattern.VerticallyScrollable:
                            box = CachedPropertyAccessor.get_bounding_rectangle(node)
                            x,y=random_point_within_bounding_box(node=node,scale_factor=0.8)
                            center = Center(x=x,y=y)
                            name = CachedPropertyAccessor.get_name(node)
                            automation_id = CachedPropertyAccessor.get_automation_id(node)
                            localized_control_type = CachedPropertyAccessor.get_localized_control_type(node)
                            has_keyboard_focus = CachedPropertyAccessor.get_has_keyboard_focus(node)
                            scrollable_nodes.append(ScrollElementNode(**{
                                'name':name.strip() or automation_id or localized_control_type.capitalize() or "''",
                                'control_type':localized_control_type.title(),
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
                                'is_focused':has_keyboard_focus
                            }))
                    except Exception:
                        pass
        
            # Interactive and Informative checks
            # Pre-calculate common properties
            is_control_element = CachedPropertyAccessor.get_is_control_element(node)
            element_bounding_box = CachedPropertyAccessor.get_bounding_rectangle(node)
            width = element_bounding_box.width()
            height = element_bounding_box.height()
            area = width * height
            
            # Is Visible Check
            is_visible = (area > 0) and (not is_offscreen or control_type_name == 'EditControl') and is_control_element
            
            if is_visible:
                is_enabled = CachedPropertyAccessor.get_is_enabled(node)
                if is_enabled:
                    # Determine is_keyboard_focusable
                    if control_type_name in set(['EditControl','ButtonControl','CheckBoxControl','RadioButtonControl','TabItemControl']):
                         is_keyboard_focusable = True
                    else:
                         is_keyboard_focusable = CachedPropertyAccessor.get_is_keyboard_focusable(node)
                    
                    # Interactive Check
                    if interactive_nodes is not None:
                        is_interactive = False
                        if is_browser and control_type_name in set(['DataItemControl','ListItemControl']) and not is_keyboard_focusable:
                            is_interactive = False
                        elif not is_browser and control_type_name == "ImageControl" and is_keyboard_focusable:
                            is_interactive = True
                        elif control_type_name in (INTERACTIVE_CONTROL_TYPE_NAMES|DOCUMENT_CONTROL_TYPE_NAMES):
                             # Role check
                             try:
                                legacy_pattern = node.GetLegacyIAccessiblePattern()
                                is_role_interactive = AccessibleRoleNames.get(legacy_pattern.Role, "Default") in INTERACTIVE_ROLES
                             except Exception:
                                is_role_interactive = False
                             
                             # Image check
                             is_image = False
                             if control_type_name == 'ImageControl': # approximated
                                 localized = CachedPropertyAccessor.get_localized_control_type(node)
                                 if localized == 'graphic' or not is_keyboard_focusable:
                                     is_image = True
                             
                             if is_role_interactive and (not is_image or is_keyboard_focusable):
                                 is_interactive = True
                                 
                        elif control_type_name == 'GroupControl':
                             if is_browser:
                                 try:
                                    legacy_pattern = node.GetLegacyIAccessiblePattern()
                                    is_role_interactive = AccessibleRoleNames.get(legacy_pattern.Role, "Default") in INTERACTIVE_ROLES
                                 except Exception:
                                    is_role_interactive = False
                                    
                                 is_default_action = False
                                 try:
                                     legacy_pattern = node.GetLegacyIAccessiblePattern()
                                     if legacy_pattern.DefaultAction.title() in DEFAULT_ACTIONS:
                                         is_default_action = True
                                 except: pass
                                 
                                 if is_role_interactive and (is_default_action or is_keyboard_focusable):
                                     is_interactive = True

                        if is_interactive:
                            legacy_pattern=node.GetLegacyIAccessiblePattern()
                            value=legacy_pattern.Value.strip() if legacy_pattern.Value is not None else ""
                            is_focused = CachedPropertyAccessor.get_has_keyboard_focus(node)
                            name = CachedPropertyAccessor.get_name(node).strip()
                            localized_control_type = CachedPropertyAccessor.get_localized_control_type(node)
                            accelerator_key = CachedPropertyAccessor.get_accelerator_key(node)
                            
                            if is_browser and is_dom:
                                bounding_box=self.iou_bounding_box(self.dom_bounding_box,element_bounding_box)
                                center = bounding_box.get_center()
                                tree_node=TreeElementNode(**{
                                    'name':name,
                                    'control_type':localized_control_type.title(),
                                    'value':value,
                                    'shortcut':accelerator_key,
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
                                    'control_type':localized_control_type.title(),
                                    'value':value,
                                    'shortcut':accelerator_key,
                                    'bounding_box':bounding_box,
                                    'center':center,
                                    'xpath':'',
                                    'app_name':app_name,
                                    'is_focused':is_focused
                                })
                                interactive_nodes.append(tree_node)

                    # Informative Check
                    if dom_informative_nodes is not None:
                         # is_element_text check
                         is_text = False
                         if control_type_name in INFORMATIVE_CONTROL_TYPE_NAMES:
                              # is_element_image check
                              is_image_check = False
                              if control_type_name == 'ImageControl':
                                   localized = CachedPropertyAccessor.get_localized_control_type(node)
                                   
                                   # Check keybord focusable again if not established, but reuse
                                   if not is_keyboard_focusable:
                                        # If localized is graphic OR not focusable -> image
                                        # wait, is_element_image: if localized=='graphic' or not focusable -> True
                                        if localized == 'graphic':
                                             is_image_check = True
                                        else:
                                             is_image_check = True # not focusable
                                   elif localized == 'graphic': 
                                        is_image_check = True

                              if not is_image_check:
                                  is_text = True
                         
                         if is_text:
                             if is_browser and is_dom:
                                 name = CachedPropertyAccessor.get_name(node)
                                 dom_informative_nodes.append(TextElementNode(
                                     text=name.strip(),
                                 ))
            
            # Phase 3: Cached Children Retrieval
            _, children_req = self._get_thread_cache()
            children = CachedControlHelper.get_cached_children(node, children_req)
            
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
                            # Inline is_window_modal
                            is_modal = False
                            try:
                                window_pattern = child.GetWindowPattern()
                                is_modal = window_pattern.IsModal
                            except Exception:
                                pass
                                
                            if is_modal:
                                # Because this window element is modal
                                interactive_nodes.clear()
                    # enter dialog subtree
                    self.tree_traversal(child, window_bounding_box, app_name, is_browser, interactive_nodes, scrollable_nodes, dom_interactive_nodes, dom_informative_nodes, is_dom=is_dom, is_dialog=True)
                else:
                    # normal non-dialog children
                    self.tree_traversal(child, window_bounding_box, app_name, is_browser, interactive_nodes, scrollable_nodes, dom_interactive_nodes, dom_informative_nodes, is_dom=is_dom, is_dialog=is_dialog)
        except Exception as e:
            logger.error(f"Error in tree_traversal: {e}", exc_info=True)
            raise

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

    def _on_property_change(self, sender:'ctypes.POINTER(IUIAutomationElement)', propertyId:int, newValue):
        """Handle property change events."""
        try:
            element = Control.CreateControlFromElement(sender)
            logger.debug(f"[WatchDog] Property changed: ID={propertyId} Value={newValue} Element: '{element.Name}' ({element.ControlTypeName})")
        except Exception:
            pass