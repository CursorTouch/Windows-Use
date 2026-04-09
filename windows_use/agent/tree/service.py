from windows_use.uia import Control, ComboBoxControl, CheckBoxControl, EditControl, ButtonControl, SliderControl, ScrollPattern, WindowControl, Rect, ExpandCollapseState, ToggleState, PatternId, PropertyId, AccessibleRoleNames, TreeScope, ControlFromHandle
from windows_use.agent.tree.config import INTERACTIVE_CONTROL_TYPE_NAMES, DOCUMENT_CONTROL_TYPE_NAMES, INFORMATIVE_CONTROL_TYPE_NAMES, DEFAULT_ACTIONS, INTERACTIVE_ROLES, THREAD_MAX_RETRIES
from windows_use.agent.tree.views import TreeElementNode, ScrollElementNode, TextElementNode, Center, BoundingBox, TreeState
from windows_use.agent.tree.cache_utils import CacheRequestFactory, CachedControlHelper
from windows_use.agent.tree.utils import random_point_within_bounding_box
from typing import TYPE_CHECKING,Optional,Any
from time import sleep,perf_counter
import logging
import weakref
import ctypes

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


    def get_state(self,active_window_handle:int|None,other_windows_handles:list[int])->TreeState:
        # Reset DOM state to prevent leaks and stale data
        self.dom = None
        self.dom_bounding_box = None
        start_time = perf_counter()

        active_window_flag=False
        if active_window_handle:
            active_window_flag=True
            windows_handles=[active_window_handle]+other_windows_handles
        else:
            windows_handles=other_windows_handles
        
        interactive_nodes,scrollable_nodes,dom_informative_nodes,failed_handles=self.get_window_wise_nodes(windows_handles=windows_handles,active_window_flag=active_window_flag)
        root_node=TreeElementNode(
            name="Desktop",
            control_type="PaneControl",
            bounding_box=self.screen_box,
            center=self.screen_box.get_center(),
            window_name="Desktop",
            metadata={}
        )
        if self.dom:
            try:
                scroll_pattern:ScrollPattern=self.dom.GetCachedPattern(PatternId.ScrollPattern, True)
                metadata={
                    'horizontal_scrollable':scroll_pattern.HorizontallyScrollable if scroll_pattern else False,
                    'horizontal_scroll_percent':round(scroll_pattern.HorizontalScrollPercent,2) if scroll_pattern and scroll_pattern.HorizontallyScrollable else 0,
                    'vertical_scrollable':scroll_pattern.VerticallyScrollable if scroll_pattern else False,
                    'vertical_scroll_percent':round(scroll_pattern.VerticalScrollPercent,2) if scroll_pattern and scroll_pattern.VerticallyScrollable else 0,
                }
                dom_node=ScrollElementNode(**{
                    'name':'DOM',
                    'control_type':'DocumentControl',
                    'bounding_box':self.dom_bounding_box,
                    'center':self.dom_bounding_box.get_center(),
                    'window_name':'DOM',
                    'metadata':metadata
                })
            except Exception as e:
                logger.debug(f"Failed to get DOM scroll pattern: {e}")
                dom_node=None
        else:
            dom_node=None
        # Detect if tree capture failed for any windows
        status = len(failed_handles) == 0
        if not status:
            logger.warning(f"[Tree] {len(failed_handles)} window(s) failed to capture — UI services may be loading")
        end_time = perf_counter()
        logger.debug(f"[Tree] Tree State capture took {end_time - start_time:.2f} seconds")
        return TreeState(status=status,root_node=root_node,dom_node=dom_node,interactive_nodes=interactive_nodes,scrollable_nodes=scrollable_nodes,dom_informative_nodes=dom_informative_nodes)

    def get_window_wise_nodes(self,windows_handles:list[int],active_window_flag:bool) -> tuple[list[TreeElementNode],list[ScrollElementNode],list[TextElementNode],list[int]]:
        """Process windows sequentially to avoid COM apartment threading deadlock.

        UI Automation requires STA (Single-Threaded Apartment). Using ThreadPoolExecutor
        with worker threads that each call CoInitialize() creates multiple STA threads,
        causing cross-apartment marshaling deadlocks when the main thread also does
        COM operations (ControlFromHandle, is_window_browser). Sequential processing
        keeps all UIA COM calls in the main thread's STA.
        """
        interactive_nodes, scrollable_nodes, dom_informative_nodes = [], [], []
        failed_handles = []

        task_inputs = []
        for handle in windows_handles:
            is_browser = False
            try:
                temp_node = ControlFromHandle(handle)
                if active_window_flag and temp_node.ClassName == "Progman":
                    continue
                is_browser = self.desktop.is_window_browser(temp_node)
            except Exception:
                pass
            task_inputs.append((handle, is_browser))

        retry_counts = {handle: 0 for handle in windows_handles}
        for handle, is_browser in task_inputs:
            for attempt in range(THREAD_MAX_RETRIES + 1):
                try:
                    result = self.get_nodes(handle, is_browser, wait_time=0.5 * (2 ** (attempt - 1)) if attempt > 0 else 0)
                    if result:
                        element_nodes, scroll_nodes, info_nodes = result
                        interactive_nodes.extend(element_nodes)
                        scrollable_nodes.extend(scroll_nodes)
                        dom_informative_nodes.extend(info_nodes)
                    break
                except Exception as e:
                    retry_counts[handle] = attempt + 1
                    try:
                        window_name = ControlFromHandle(handle).Name
                    except Exception:
                        window_name = "Unknown"
                    logger.warning(
                        f"Error in processing window '{window_name}' (handle {handle}), "
                        f"retry attempt {retry_counts[handle]}/{THREAD_MAX_RETRIES}\nError: {e}"
                    )
                    if attempt < THREAD_MAX_RETRIES:
                        wait_time = 0.5 * (2 ** attempt)
                        logger.debug(f"Retrying window {handle} in {wait_time}s...")
                        sleep(wait_time)
                    else:
                        logger.error(f"Task failed completely for handle {handle} after {THREAD_MAX_RETRIES} retries")
                        failed_handles.append(handle)
                        break

        return interactive_nodes, scrollable_nodes, dom_informative_nodes, failed_handles
    
    def iou_bounding_box(self, window_box: Rect, element_box: Rect) -> BoundingBox:
        clipped = element_box.intersect(window_box).intersect(self.screen_box)
        if clipped.right > clipped.left and clipped.bottom > clipped.top:
            return BoundingBox(
                left=clipped.left,
                top=clipped.top,
                right=clipped.right,
                bottom=clipped.bottom,
                width=clipped.width(),
                height=clipped.height()
            )
        return BoundingBox(left=0, top=0, right=0, bottom=0, width=0, height=0)



    def element_has_child_element(self, node:Control,control_type:str,child_control_type:str):
        # node is cached — use cached property
        if node.CachedLocalizedControlType==control_type:
            first_child=node.GetFirstChildControl()
            if first_child is None:
                return False
            # first_child from GetFirstChildControl() is NOT cached — use live access
            return first_child.LocalizedControlType==child_control_type

    def _dom_correction(self, node:Control, dom_interactive_nodes:list[TreeElementNode], window_name:str):
        if self.element_has_child_element(node,'list item','link') or self.element_has_child_element(node,'item','link') or self.element_has_child_element(node,"option","button"):
            dom_interactive_nodes.pop()
            return None
        elif node.CachedControlTypeName=='GroupControl':
            popped=dom_interactive_nodes.pop()
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
                        # Children from GetFirstChildControl() are NOT cached — use live access
                        if child.ControlTypeName in INTERACTIVE_CONTROL_TYPE_NAMES:
                            return None
                        child=child.GetFirstChildControl()
                except Exception:
                    return None
                if child.ControlTypeName!='TextControl':
                    return None
                metadata:dict[str,Any]={}
                # node is cached — use cached properties
                element_bounding_box = node.CachedBoundingRectangle
                bounding_box=self.iou_bounding_box(self.dom_bounding_box,element_bounding_box)
                center = bounding_box.get_center()
                has_focused=node.CachedHasKeyboardFocus
                accelerator_key=node.CachedAcceleratorKey
                metadata['has_focused']=has_focused
                if accelerator_key:
                    metadata['shortcut']=accelerator_key

                if isinstance(node,EditControl):
                    try:
                        value = node.GetCachedPropertyValue(PropertyId.LegacyIAccessibleValueProperty)
                        metadata['value']=value.strip() if value else '(empty)'
                    except Exception:
                        pass
                    
                    try:
                        help_text = node.CachedHelpText
                        if help_text:
                            metadata['help_text']=help_text.encode('ascii', 'ignore').decode('ascii')
                    except Exception:
                        pass

                dom_interactive_nodes.append(TreeElementNode(**{
                    'name':(child.Name or '').strip(),
                    'control_type':node.CachedLocalizedControlType,
                    'bounding_box':bounding_box,
                    'center':center,
                    'window_name':window_name,
                    'hwnd':popped.hwnd,
                    'control':node,
                    'metadata':metadata
                }))
        elif self.element_has_child_element(node,'link','heading'):
            popped=dom_interactive_nodes.pop()
            # child from GetFirstChildControl() is NOT cached — use live access
            node=node.GetFirstChildControl()
            control_type='link'
            value = node.GetPropertyValue(PropertyId.LegacyIAccessibleValueProperty) or ''
            element_bounding_box = node.BoundingRectangle
            bounding_box=self.iou_bounding_box(self.dom_bounding_box,element_bounding_box)
            center = bounding_box.get_center()
            is_focused=node.HasKeyboardFocus
            metadata:dict[str,Any]={}
            metadata['has_focused']=is_focused
            dom_interactive_nodes.append(TreeElementNode(**{
                'name':(node.Name or '').strip(),
                'control_type':control_type,
                'bounding_box':bounding_box,
                'center':center,
                'window_name':window_name,
                'hwnd':popped.hwnd,
                'control':node,
                'metadata':metadata
            }))


    def tree_traversal(self, node: Control, window_bounding_box:Rect, window_name:str, is_browser:bool,
                    interactive_nodes:Optional[list[TreeElementNode]]=None, scrollable_nodes:Optional[list[ScrollElementNode]]=None,
                    dom_interactive_nodes:Optional[list[TreeElementNode]]=None, dom_informative_nodes:Optional[list[TextElementNode]]=None,
                    is_dom:bool=False, is_dialog:bool=False,
                    element_cache_req:Optional[Any]=None, children_cache_req:Optional[Any]=None,
                    hwnd:int=0):
        try:
            # Build cached control if caching is enabled
            if not hasattr(node, '_is_cached') and element_cache_req:
                node = CachedControlHelper.build_cached_control(node, element_cache_req)
            
            # Checks to skip the nodes that are not interactive
            is_offscreen = node.CachedIsOffscreen
            control_type_name = node.CachedControlTypeName
            # class_name = node.CachedClassName
            
            # Scrollable check
            if scrollable_nodes is not None:
                if (control_type_name not in (INTERACTIVE_CONTROL_TYPE_NAMES|INFORMATIVE_CONTROL_TYPE_NAMES)) and not is_offscreen:
                    try:
                        scroll_pattern:ScrollPattern=node.GetCachedPattern(PatternId.ScrollPattern, True)
                        if scroll_pattern and scroll_pattern.VerticallyScrollable:
                            box = node.CachedBoundingRectangle
                            x,y=random_point_within_bounding_box(node=node,scale_factor=0.8)
                            center = Center(x=x,y=y)
                            name = node.CachedName
                            automation_id = node.CachedAutomationId
                            localized_control_type = node.CachedLocalizedControlType
                            metadata:dict[str,Any]={}
                            metadata['has_focused']=node.CachedHasKeyboardFocus
                            scrollable_nodes.append(ScrollElementNode(**{
                                'name':(name or '').strip() or automation_id or localized_control_type.capitalize() or "''",
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
                                'horizontal_scrollable':scroll_pattern.HorizontallyScrollable,
                                'horizontal_scroll_percent':round(scroll_pattern.HorizontalScrollPercent,2) if scroll_pattern.HorizontallyScrollable else 0,
                                'vertical_scrollable':scroll_pattern.VerticallyScrollable,
                                'vertical_scroll_percent':round(scroll_pattern.VerticalScrollPercent,2) if scroll_pattern.VerticallyScrollable else 0,
                                'window_name':window_name,
                                'hwnd':hwnd,
                                'control':node,
                                'metadata':metadata
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
            is_visible = (area > 0) and (not is_offscreen or control_type_name=="EditControl" or (control_type_name=="ListItemControl" and is_browser)) and is_control_element
            
            if is_visible:
                is_enabled = node.CachedIsEnabled
                if is_enabled:
                    # Determine is_keyboard_focusable
                    if control_type_name in set(['EditControl','ButtonControl','CheckBoxControl','RadioButtonControl','TabItemControl','ListItemControl']):
                        is_keyboard_focusable = True
                    else:
                        #Experimentally, ListItemControl is keyboard focusable
                        is_keyboard_focusable = node.CachedIsKeyboardFocusable
                    
                    # Interactive Check
                    if interactive_nodes is not None:
                        is_interactive = False
                        if is_browser and control_type_name in set(['DataItemControl']) and not is_keyboard_focusable:
                            is_interactive = False
                        elif not is_browser and control_type_name == "ImageControl" and is_keyboard_focusable:
                            is_interactive = True
                        elif control_type_name in (INTERACTIVE_CONTROL_TYPE_NAMES|DOCUMENT_CONTROL_TYPE_NAMES):
                             # Role check
                             try:
                                role = node.GetCachedPropertyValue(PropertyId.LegacyIAccessibleRoleProperty)
                                is_role_interactive = AccessibleRoleNames.get(role, "Default") in INTERACTIVE_ROLES
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
                                    role = node.GetCachedPropertyValue(PropertyId.LegacyIAccessibleRoleProperty)
                                    is_role_interactive = AccessibleRoleNames.get(role, "Default") in INTERACTIVE_ROLES
                                 except Exception:
                                    is_role_interactive = False
                                    
                                 is_default_action = False
                                 try:
                                     default_action = node.GetCachedPropertyValue(PropertyId.LegacyIAccessibleDefaultActionProperty)
                                     if default_action and default_action.title() in DEFAULT_ACTIONS:
                                         is_default_action = True
                                 except Exception:
                                    pass
                                 
                                 if is_role_interactive and (is_default_action or is_keyboard_focusable):
                                     is_interactive = True

                        if is_interactive:
                            is_focused = node.CachedHasKeyboardFocus
                            name = (node.CachedName or '').strip()
                            localized_control_type = node.CachedLocalizedControlType
                            accelerator_key = node.CachedAcceleratorKey

                            metadata:dict[str,Any]={}
                            metadata['has_focused']=is_focused
                            if accelerator_key:
                                metadata['shortcut']=accelerator_key
                            
                            try:
                                help_text = node.CachedHelpText
                                if help_text:
                                    metadata['help_text']=help_text.encode('ascii', 'ignore').decode('ascii')
                            except Exception:
                                pass

                            if isinstance(node,(ButtonControl,CheckBoxControl)):
                                try:
                                    toggle_state = node.GetCachedPropertyValue(PropertyId.ToggleToggleStateProperty)
                                    if toggle_state is not None:
                                        match toggle_state:
                                            case ToggleState.On:
                                                metadata['toggle_state'] = 'on'
                                            case ToggleState.Off:
                                                metadata['toggle_state'] = 'off'
                                            case _:
                                                pass
                                except Exception:
                                    pass

                            if isinstance(node,EditControl):
                                try:
                                    value = node.GetCachedPropertyValue(PropertyId.LegacyIAccessibleValueProperty)
                                    metadata['value']=value.strip() if value else '(empty)'
                                except Exception:
                                    pass

                                try:
                                    if node.CachedIsPassword:
                                        metadata['is_password']=True
                                except Exception:
                                    pass
                            
                            if isinstance(node,ComboBoxControl):
                                try:
                                    control_state=node.GetCachedPropertyValue(PropertyId.ExpandCollapseExpandCollapseStateProperty)
                                    match control_state:
                                        case ExpandCollapseState.Expanded:
                                            metadata['expand_collapse_state']='expanded'
                                        case ExpandCollapseState.Collapsed:
                                            metadata['expand_collapse_state']='collapsed'
                                        case ExpandCollapseState.PartiallyExpanded:
                                            metadata['expand_collapse_state']='partially expanded'
                                        case _:
                                            pass
                                except Exception:
                                    pass

                                try: 
                                    can_select_multiple=node.GetCachedPropertyValue(PropertyId.SelectionCanSelectMultipleProperty)
                                    metadata['is_selection_required']=can_select_multiple
                                except Exception:
                                    pass

                                try:
                                    is_selection_required=node.GetCachedPropertyValue(PropertyId.SelectionIsSelectionRequiredProperty)
                                    metadata['is_selection_required']=is_selection_required
                                except Exception:
                                    pass

                                try:
                                    is_selected=node.GetCachedPropertyValue(PropertyId.SelectionItemIsSelectedProperty)
                                    metadata['is_selected']=is_selected
                                except Exception:
                                    pass

                                try:
                                    selection_raw = node.GetCachedPropertyValue(PropertyId.SelectionSelectionProperty)
                                    selected_items = Control.CreateControlsFromRawElementArray(selection_raw)
                                    selected_names = [item.Name for item in selected_items if item.Name]
                                    if selected_names:
                                        metadata['selection'] = selected_names
                                except Exception:
                                    pass

                            if isinstance(node, SliderControl):
                                try:
                                    value = node.GetCachedPropertyValue(PropertyId.RangeValueValueProperty)
                                    minimum = node.GetCachedPropertyValue(PropertyId.RangeValueMinimumProperty)
                                    maximum = node.GetCachedPropertyValue(PropertyId.RangeValueMaximumProperty)
                                    if value is not None:
                                        metadata['value'] = round(value, 2)
                                    if minimum is not None:
                                        metadata['min'] = round(minimum, 2)
                                    if maximum is not None:
                                        metadata['max'] = round(maximum, 2)
                                except Exception:
                                    pass

                            if is_browser and is_dom:
                                bounding_box=self.iou_bounding_box(self.dom_bounding_box,element_bounding_box)
                                center = bounding_box.get_center()
                                tree_node=TreeElementNode(**{
                                    'name':name,
                                    'control_type':localized_control_type.title(),
                                    'bounding_box':bounding_box,
                                    'center':center,
                                    'window_name':window_name,
                                    'hwnd':hwnd,
                                    'control':node,
                                    'metadata':metadata
                                })
                                dom_interactive_nodes.append(tree_node)
                                self._dom_correction(node, dom_interactive_nodes, window_name)
                            else:
                                bounding_box=self.iou_bounding_box(window_bounding_box,element_bounding_box)
                                center = bounding_box.get_center()
                                tree_node=TreeElementNode(**{
                                    'name':name,
                                    'control_type':localized_control_type.title(),
                                    'bounding_box':bounding_box,
                                    'center':center,
                                    'window_name':window_name,
                                    'hwnd':hwnd,
                                    'control':node,
                                    'metadata':metadata
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
                                   
                                   if not is_keyboard_focusable:
                                        if localized == 'graphic':
                                             is_image_check = True
                                        else:
                                             is_image_check = True
                                   elif localized == 'graphic': 
                                        is_image_check = True

                              if not is_image_check:
                                  is_text = True
                         
                         if is_text:
                             if is_browser and is_dom:
                                 name = node.CachedName
                                 dom_informative_nodes.append(TextElementNode(
                                     text=(name or '').strip(),
                                 ))
            
            # Phase 3: Cached Children Retrieval
            children = CachedControlHelper.get_cached_children(node, children_cache_req)

            # enumerate preserves original index so reversed iteration still maps correctly
            traversal = list(enumerate(children))
            if not is_dom:
                traversal = list(reversed(traversal))

            for orig_idx, child in traversal:
                # Check if the child is a DOM element
                if is_browser and child.CachedAutomationId=="RootWebArea":
                    bounding_box=child.CachedBoundingRectangle
                    self.dom_bounding_box=BoundingBox(left=bounding_box.left,top=bounding_box.top,
                    right=bounding_box.right,bottom=bounding_box.bottom,width=bounding_box.width(),
                    height=bounding_box.height())
                    self.dom=child
                    # enter DOM subtree
                    self.tree_traversal(child, window_bounding_box, window_name, is_browser, interactive_nodes, scrollable_nodes, dom_interactive_nodes, dom_informative_nodes, is_dom=True, is_dialog=is_dialog, element_cache_req=element_cache_req, children_cache_req=children_cache_req, hwnd=hwnd)
                # Check if the child is a dialog
                elif isinstance(child,WindowControl):
                    if not child.CachedIsOffscreen:
                        if is_dom:
                            bounding_box=child.CachedBoundingRectangle
                            if bounding_box.width() > 0.8*self.dom_bounding_box.width:
                                # Because this window element covers the majority of the screen
                                dom_interactive_nodes.clear()
                        else:
                            # Inline is_window_modal
                            is_modal = False
                            try:
                                is_modal = child.GetCachedPropertyValue(PropertyId.WindowIsModalProperty)
                            except Exception:
                                is_modal = False

                            if is_modal:
                                interactive_nodes.clear()
                    # enter dialog subtree
                    self.tree_traversal(child, window_bounding_box, window_name, is_browser, interactive_nodes, scrollable_nodes, dom_interactive_nodes, dom_informative_nodes, is_dom=is_dom, is_dialog=True, element_cache_req=element_cache_req, children_cache_req=children_cache_req, hwnd=hwnd)
                else:
                    # normal non-dialog children
                    self.tree_traversal(child, window_bounding_box, window_name, is_browser, interactive_nodes, scrollable_nodes, dom_interactive_nodes, dom_informative_nodes, is_dom=is_dom, is_dialog=is_dialog, element_cache_req=element_cache_req, children_cache_req=children_cache_req, hwnd=hwnd)
        except Exception as e:
            logger.error(f"Error in tree_traversal: {e}", exc_info=True)
            raise

    def window_name_correction(self,window_name:str)->str:
        match window_name:
            case "Progman":
                return "Desktop"
            case 'Shell_TrayWnd'|'Shell_SecondaryTrayWnd':
                return "Taskbar"
            case 'Microsoft.UI.Content.PopupWindowSiteBridge':
                return "Context Menu"
            case _:
                return window_name
    
    def get_nodes(self, handle: int, is_browser:bool=False, wait_time:float=0) -> tuple[list[TreeElementNode],list[ScrollElementNode],list[TextElementNode]]:
        if wait_time > 0:
            sleep(wait_time)
        try:
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
            window_name=(node.Name or '').strip()
            window_name=self.window_name_correction(window_name)

            self.tree_traversal(node, window_bounding_box, window_name, is_browser, interactive_nodes, scrollable_nodes, dom_interactive_nodes, dom_informative_nodes, is_dom=False, is_dialog=False, element_cache_req=element_cache_req, children_cache_req=children_cache_req, hwnd=handle)
            logger.debug(f'Window name:{window_name}')
            logger.debug(f'Interactive nodes:{len(interactive_nodes)}')
            if is_browser:
                logger.debug(f'DOM interactive nodes:{len(dom_interactive_nodes)}')
                logger.debug(f'DOM informative nodes:{len(dom_informative_nodes)}')
            logger.debug(f'Scrollable nodes:{len(scrollable_nodes)}')

            interactive_nodes.extend(dom_interactive_nodes)
            return (interactive_nodes,scrollable_nodes,dom_informative_nodes)
        except Exception as e:
            logger.error(f"Error getting nodes for handle {handle}: {e}")
            raise

    def on_focus_change(self, sender:ctypes.POINTER('IUIAutomationElement')):
        """Handle focus change events."""
        # Debounce duplicate events
        current_time = perf_counter()
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
