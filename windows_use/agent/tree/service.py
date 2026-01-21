from windows_use.uia import Control,ImageControl,ScrollPattern,WindowControl,Rect,GetRootControl,PatternId,AccessibleRoleNames,PaneControl,GroupControl,StructureChangeType,TreeScope,ControlFromHandle
from windows_use.agent.tree.config import INTERACTIVE_CONTROL_TYPE_NAMES,DOCUMENT_CONTROL_TYPE_NAMES,INFORMATIVE_CONTROL_TYPE_NAMES, DEFAULT_ACTIONS, INTERACTIVE_ROLES, THREAD_MAX_RETRIES
from windows_use.agent.tree.views import TreeElementNode, ScrollElementNode, TextElementNode, Center, BoundingBox, TreeState
from windows_use.agent.tree.cache_utils import CacheRequestFactory,CachedControlHelper
from windows_use.agent.tree.utils import random_point_within_bounding_box
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import TYPE_CHECKING,Optional,Any
from time import sleep,time
import threading
import logging
import random
import weakref
import comtypes

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if TYPE_CHECKING:
    from windows_use.agent.desktop.service import Desktop
    
class Tree:
    def __init__(self,desktop:'Desktop'):
        self.desktop=weakref.proxy(desktop)
        self.screen_size=desktop.get_screen_size()
        self.dom:Optional[Control]=None
        self.dom_bounding_box:BoundingBox=None
        self.screen_box=BoundingBox(
            top=0, left=0, bottom=self.screen_size.height, right=self.screen_size.width,
            width=self.screen_size.width, height=self.screen_size.height
        )
        self.tree_state=None


    def get_state(self,active_app_handle:int|None,other_apps_handles:list[int])->TreeState:
        # Reset DOM state to prevent leaks and stale data
        self.dom = None
        self.dom_bounding_box = None
        start_time = time()

        active_app_flag=False
        if active_app_handle:
            active_app_flag=True
            apps_handles=[active_app_handle]+other_apps_handles
        else:
            apps_handles=other_apps_handles
        
        interactive_nodes,scrollable_nodes,dom_informative_nodes=self.get_appwise_nodes(apps_handles=apps_handles,active_app_flag=active_app_flag)
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
        end_time = time()
        logger.info(f"Tree State capture took {end_time - start_time:.2f} seconds")
        return self.tree_state

    def get_appwise_nodes(self,apps_handles:list[int],active_app_flag:bool) -> tuple[list[TreeElementNode],list[ScrollElementNode],list[TextElementNode]]:
        interactive_nodes, scrollable_nodes, dom_informative_nodes = [], [], []
        
        # Pre-calculate browser status in main thread to pass simple types to workers
        task_inputs = []
        for handle in apps_handles:
            is_browser = False
            try:
                # Use temporary control for property check in main thread
                # This is safe as we don't pass this specific COM object to the thread
                temp_node = ControlFromHandle(handle)
                if active_app_flag and temp_node.ClassName=='Progman':
                    continue
                is_browser = self.desktop.is_app_browser(temp_node)
            except Exception:
                pass
            task_inputs.append((handle, is_browser))

        with ThreadPoolExecutor() as executor:
            retry_counts = {handle: 0 for handle in apps_handles}
            future_to_handle = {
                executor.submit(self.get_nodes, handle, is_browser): handle
                for handle, is_browser in task_inputs
            }
            while future_to_handle:  # keep running until no pending futures
                for future in as_completed(list(future_to_handle)):
                    handle = future_to_handle.pop(future)  # remove completed future
                    try:
                        result = future.result()
                        if result:
                            element_nodes, scroll_nodes, info_nodes = result
                            interactive_nodes.extend(element_nodes)
                            scrollable_nodes.extend(scroll_nodes)
                            dom_informative_nodes.extend(info_nodes)
                    except Exception as e:
                        retry_counts[handle] += 1
                        logger.debug(f"Error in processing handle {handle}, retry attempt {retry_counts[handle]}\nError: {e}")
                        if retry_counts[handle] < THREAD_MAX_RETRIES:
                            # Need to find is_browser again for retry
                            is_browser = next((ib for h, ib in task_inputs if h == handle), False)
                            new_future = executor.submit(self.get_nodes, handle, is_browser)
                            future_to_handle[new_future] = handle
                        else:
                            logger.error(f"Task failed completely for handle {handle} after {THREAD_MAX_RETRIES} retries")
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
            control_type_name_check = node.CachedControlTypeName
            is_kb_focusable = False
            if control_type_name_check in set(['EditControl','ButtonControl','CheckBoxControl','RadioButtonControl','TabItemControl']):
                 is_kb_focusable = True
            else:
                 is_kb_focusable = node.CachedIsKeyboardFocusable

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
                    is_dom:bool=False, is_dialog:bool=False,
                    element_cache_req:Optional[Any]=None, children_cache_req:Optional[Any]=None):
        try:
            # Build cached control if caching is enabled
            if not hasattr(node, '_is_cached') and element_cache_req:
                node = CachedControlHelper.build_cached_control(node, element_cache_req)
            
            # Checks to skip the nodes that are not interactive
            is_offscreen = node.CachedIsOffscreen
            control_type_name = node.CachedControlTypeName
            class_name = node.CachedClassName
            
            # Scrollable check
            if scrollable_nodes is not None:
                if (control_type_name not in (INTERACTIVE_CONTROL_TYPE_NAMES|INFORMATIVE_CONTROL_TYPE_NAMES)) and not is_offscreen:
                    try:
                        scroll_pattern:ScrollPattern=node.GetPattern(PatternId.ScrollPattern)
                        if scroll_pattern and scroll_pattern.VerticallyScrollable:
                            box = node.CachedBoundingRectangle
                            x,y=random_point_within_bounding_box(node=node,scale_factor=0.8)
                            center = Center(x=x,y=y)
                            name = node.CachedName
                            automation_id = node.CachedAutomationId
                            localized_control_type = node.CachedLocalizedControlType
                            has_keyboard_focus = node.CachedHasKeyboardFocus
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
            is_control_element = node.CachedIsControlElement
            element_bounding_box = node.CachedBoundingRectangle
            width = element_bounding_box.width()
            height = element_bounding_box.height()
            area = width * height
            
            # Is Visible Check
            is_visible = (area > 0) and (not is_offscreen or control_type_name == 'EditControl') and is_control_element
            
            if is_visible:
                is_enabled = node.CachedIsEnabled
                if is_enabled:
                    # Determine is_keyboard_focusable
                    if control_type_name in set(['EditControl','ButtonControl','CheckBoxControl','RadioButtonControl','TabItemControl']):
                         is_keyboard_focusable = True
                    else:
                         is_keyboard_focusable = node.CachedIsKeyboardFocusable
                    
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
                                 localized = node.CachedLocalizedControlType
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
                            is_focused = node.CachedHasKeyboardFocus
                            name = node.CachedName.strip()
                            localized_control_type = node.CachedLocalizedControlType
                            accelerator_key = node.CachedAcceleratorKey
                            
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
                                   localized = node.CachedLocalizedControlType
                                   
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
                                 name = node.CachedName
                                 dom_informative_nodes.append(TextElementNode(
                                     text=name.strip(),
                                 ))
            
            # Phase 3: Cached Children Retrieval
            children = CachedControlHelper.get_cached_children(node, children_cache_req)
            
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
                    self.tree_traversal(child, window_bounding_box, app_name, is_browser, interactive_nodes, scrollable_nodes, dom_interactive_nodes, dom_informative_nodes, is_dom=True, is_dialog=is_dialog, element_cache_req=element_cache_req, children_cache_req=children_cache_req)
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
                    self.tree_traversal(child, window_bounding_box, app_name, is_browser, interactive_nodes, scrollable_nodes, dom_interactive_nodes, dom_informative_nodes, is_dom=is_dom, is_dialog=True, element_cache_req=element_cache_req, children_cache_req=children_cache_req)
                else:
                    # normal non-dialog children
                    self.tree_traversal(child, window_bounding_box, app_name, is_browser, interactive_nodes, scrollable_nodes, dom_interactive_nodes, dom_informative_nodes, is_dom=is_dom, is_dialog=is_dialog, element_cache_req=element_cache_req, children_cache_req=children_cache_req)
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
    
    def get_nodes(self, handle: int, is_browser:bool=False) -> tuple[list[TreeElementNode],list[ScrollElementNode],list[TextElementNode]]:
        try:
            comtypes.CoInitialize()
            # Rehydrate Control from handle within the thread's COM context
            node = ControlFromHandle(handle)
            if not node:
                 raise Exception("Failed to create Control from handle")

            # Create fresh cache requests for this traversal session
            element_cache_req = CacheRequestFactory.create_tree_traversal_cache()
            element_cache_req.TreeScope = TreeScope.TreeScope_Element
            
            children_cache_req = CacheRequestFactory.create_tree_traversal_cache()
            children_cache_req.TreeScope = TreeScope.TreeScope_Element | TreeScope.TreeScope_Children

            window_bounding_box=node.BoundingRectangle
            
            interactive_nodes, dom_interactive_nodes, dom_informative_nodes, scrollable_nodes = [], [], [], []
            app_name=node.Name.strip()
            app_name=self.app_name_correction(app_name)

            self.tree_traversal(node, window_bounding_box, app_name, is_browser, interactive_nodes, scrollable_nodes, dom_interactive_nodes, dom_informative_nodes, is_dom=False, is_dialog=False, element_cache_req=element_cache_req, children_cache_req=children_cache_req)
            logger.debug(f'App name:{app_name}')
            logger.debug(f'Interactive nodes:{len(interactive_nodes)}')
            if is_browser:
                logger.debug(f'DOM interactive nodes:{len(dom_interactive_nodes)}')
                logger.debug(f'DOM informative nodes:{len(dom_informative_nodes)}')
            logger.debug(f'Scrollable nodes:{len(scrollable_nodes)}')

            interactive_nodes.extend(dom_interactive_nodes)
            return (interactive_nodes,scrollable_nodes,dom_informative_nodes)
        except Exception as e:
            logger.error(f"Error getting nodes for {node.Name}: {e}")
            raise e
        finally:
            comtypes.CoUninitialize()

    def _on_focus_change(self, sender:'ctypes.POINTER(IUIAutomationElement)'):
        """Handle focus change events."""
        # Debounce duplicate events
        current_time = time()
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