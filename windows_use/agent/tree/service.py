from windows_use.agent.tree.config import INTERACTIVE_CONTROL_TYPE_NAMES,INFORMATIVE_CONTROL_TYPE_NAMES, DEFAULT_ACTIONS, THREAD_MAX_RETRIES
from windows_use.agent.tree.views import TreeElementNode, TextElementNode, ScrollElementNode, Center, BoundingBox, TreeState
from uiautomation import Control,ImageControl,ScrollPattern,WindowControl,Rect
from windows_use.agent.tree.utils import random_point_within_bounding_box
from windows_use.agent.desktop.config import AVOIDED_APPS, EXCLUDED_APPS
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image, ImageFont, ImageDraw
from typing import TYPE_CHECKING
from time import sleep
import random

if TYPE_CHECKING:
    from windows_use.agent.desktop.service import Desktop
    
class Tree:
    def __init__(self,desktop:'Desktop'):
        self.desktop=desktop
        screen_size=self.desktop.get_screen_size()
        self.dom_bounding_box:BoundingBox=None
        self.screen_box=BoundingBox(
            top=0, left=0, bottom=screen_size.height, right=screen_size.width,
            width=screen_size.width, height=screen_size.height 
        )

    def get_state(self,root:Control)->TreeState:
        sleep(0.1)
        interactive_nodes,informative_nodes,scrollable_nodes=self.get_appwise_nodes(node=root)
        return TreeState(interactive_nodes=interactive_nodes,informative_nodes=informative_nodes,scrollable_nodes=scrollable_nodes)

    def get_appwise_nodes(self,node:Control) -> tuple[list[TreeElementNode],list[TextElementNode],list[ScrollElementNode]]:
        apps:list[tuple[Control,int]]=[]
        found_foreground_app=False

        EXCLUDED_APPS.discard('Progman')
        type_to_count={}
        for app in node.GetChildren():
            control_type=app.ControlTypeName
            # counting control types in the app
            type_to_count[control_type]=type_to_count.get(control_type,0)+1
            if app.ClassName in EXCLUDED_APPS:
                apps.append((app,type_to_count[control_type]))
            elif app.ClassName not in AVOIDED_APPS and self.desktop.is_app_visible(app):
                if not found_foreground_app:
                    apps.append((app,type_to_count[control_type]))
                    found_foreground_app=True
    
        interactive_nodes, informative_nodes, scrollable_nodes = [], [], []

        with ThreadPoolExecutor() as executor:
            retry_counts = {app: 0 for app,_ in apps}
            is_browser=self.desktop.is_app_browser(app)
            future_to_app = {executor.submit(self.get_nodes, app, f"{node.ControlTypeName}/{app.ControlTypeName}[{index}]", is_browser): app for app,index in apps}
            while future_to_app:  # keep running until no pending futures
                for future in as_completed(list(future_to_app)):
                    app = future_to_app.pop(future)  # remove completed future
                    try:
                        result = future.result()
                        if result:
                            element_nodes, text_nodes, scroll_nodes = result
                            interactive_nodes.extend(element_nodes)
                            informative_nodes.extend(text_nodes)
                            scrollable_nodes.extend(scroll_nodes)
                    except Exception as e:
                        retry_counts[app] += 1
                        print(f"Error in processing node {app.Name}, retry attempt {retry_counts[app]}\nError: {e}")
                        if retry_counts[app] < THREAD_MAX_RETRIES:
                            new_future = executor.submit(self.get_nodes, app, self.desktop.is_app_browser(app))
                            future_to_app[new_future] = app
                        else:
                            print(f"Task failed completely for {app.Name} after {THREAD_MAX_RETRIES} retries")
        return interactive_nodes,informative_nodes,scrollable_nodes
    
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


    def get_nodes(self, node: Control, current_xpath: str, is_browser=False) -> tuple[list[TreeElementNode],list[TextElementNode],list[ScrollElementNode]]:
        window_bounding_box=node.BoundingRectangle

        def is_element_visible(node:Control,threshold:int=0):
            is_control=node.IsControlElement
            box=node.BoundingRectangle
            if box.isempty():
                return False
            width=box.width()
            height=box.height()
            area=width*height
            is_offscreen=(not node.IsOffscreen) or node.ControlTypeName in ['EditControl']
            return area > threshold and is_offscreen and is_control
    
        def is_element_enabled(node:Control):
            try:
                return node.IsEnabled
            except Exception:
                return False
            
        def is_default_action(node:Control):
            legacy_pattern=node.GetLegacyIAccessiblePattern()
            default_action=legacy_pattern.DefaultAction.title()
            if default_action in DEFAULT_ACTIONS:
                return True
            return False
        
        def is_element_image(node:Control):
            if isinstance(node,ImageControl):
                if node.LocalizedControlType=='graphic' or not node.IsKeyboardFocusable:
                    return True
            return False
        
        def is_element_text(node:Control):
            try:
                if node.ControlTypeName in INFORMATIVE_CONTROL_TYPE_NAMES:
                    if is_element_visible(node) and is_element_enabled(node) and not is_element_image(node):
                        return True
            except Exception:
                return False
            return False
        
        def is_element_scrollable(node:Control):
            try:
                scroll_pattern:ScrollPattern=node.GetScrollPattern()
                return scroll_pattern.VerticallyScrollable or scroll_pattern.HorizontallyScrollable
            except Exception:
                return False
            
        def is_keyboard_focusable(node:Control):
            try:
                if node.ControlTypeName in set(['EditControl','ButtonControl','CheckBoxControl','RadioButtonControl','TabItemControl']):
                    return True
                return node.IsKeyboardFocusable
            except Exception:
                return False
            
        def element_has_child_element(node:Control,control_type:str,child_control_type:str):
            if node.LocalizedControlType==control_type:
                first_child=node.GetFirstChildControl()
                if first_child is None:
                    return False
                return first_child.LocalizedControlType==child_control_type
            
        def group_has_no_name(node:Control):
            try:
                if node.ControlTypeName=='GroupControl':
                    if not node.Name.strip():
                        return True
                return False
            except Exception:
                return False
            
        def is_element_interactive(node:Control):
            try:
                if is_browser and node.ControlTypeName in set(['DataItemControl','ListItemControl']) and not is_keyboard_focusable(node):
                    return False
                elif not is_browser and node.ControlTypeName=="ImageControl" and is_keyboard_focusable(node):
                    return True
                elif node.ControlTypeName in INTERACTIVE_CONTROL_TYPE_NAMES:
                    return is_element_visible(node) and is_element_enabled(node) and (not is_element_image(node) or is_keyboard_focusable(node))
                elif is_browser and node.ControlTypeName=='GroupControl':
                    return is_element_visible(node) and is_element_enabled(node) and (is_default_action(node) or is_keyboard_focusable(node))
                # elif node.ControlTypeName=='GroupControl' and not is_browser:
                #     if is_element_visible and is_element_enabled(node) and is_default_action(node):
                #         return True
            except Exception:
                return False
            return False
        
        def dom_correction(node:Control):
            if element_has_child_element(node,'list item','link') or element_has_child_element(node,'item','link'):
                dom_interactive_nodes.pop()
                return None
            elif node.ControlTypeName=='GroupControl':
                dom_interactive_nodes.pop()
                if is_keyboard_focusable(node):
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
                    dom_interactive_nodes.append(TreeElementNode(
                        name=child.Name.strip(),
                        control_type=node.LocalizedControlType,
                        value=value,
                        shortcut=node.AcceleratorKey,
                        bounding_box=bounding_box,
                        xpath='',
                        center=center,
                        app_name=app_name
                    ))
            elif element_has_child_element(node,'link','heading'):
                dom_interactive_nodes.pop()
                node=node.GetFirstChildControl()
                control_type='link'
                legacy_pattern=node.GetLegacyIAccessiblePattern()
                value=legacy_pattern.Value
                element_bounding_box = node.BoundingRectangle
                bounding_box=self.iou_bounding_box(self.dom_bounding_box,element_bounding_box)
                center = bounding_box.get_center()
                dom_interactive_nodes.append(TreeElementNode(
                    name=node.Name.strip(),
                    control_type=control_type,
                    value=node.Name.strip(),
                    shortcut=node.AcceleratorKey,
                    bounding_box=bounding_box,
                    xpath='',
                    center=center,
                    app_name=app_name
                ))
            
        def tree_traversal(node: Control, current_xpath:str,is_dom=False,is_dialog=False):
            # Checks to skip the nodes that are not interactive
            if node.IsOffscreen and (node.ControlTypeName not in set(["EditControl","TitleBarControl"])) and node.ClassName not in set(["Popup","Windows.UI.Core.CoreComponentInputSource"]):
                return None
            
            if is_element_scrollable(node):
                scroll_pattern:ScrollPattern=node.GetScrollPattern()
                box = node.BoundingRectangle
                # Get the center
                x,y=random_point_within_bounding_box(node=node,scale_factor=0.8)
                center = Center(x=x,y=y)
                scrollable_nodes.append(ScrollElementNode(
                    name=node.Name.strip() or node.LocalizedControlType.capitalize() or "''",
                    app_name=app_name,
                    control_type=node.LocalizedControlType.title(),
                    bounding_box=BoundingBox(
                        left=box.left,
                        top=box.top,
                        right=box.right,
                        bottom=box.bottom,
                        width=box.width(),
                        height=box.height()
                    ),
                    center=center,
                    xpath=current_xpath,
                    horizontal_scrollable=scroll_pattern.HorizontallyScrollable,
                    horizontal_scroll_percent=scroll_pattern.HorizontalScrollPercent if scroll_pattern.HorizontallyScrollable else 0,
                    vertical_scrollable=scroll_pattern.VerticallyScrollable,
                    vertical_scroll_percent=scroll_pattern.VerticalScrollPercent if scroll_pattern.VerticallyScrollable else 0,
                    is_focused=node.HasKeyboardFocus
                ))
            elif is_element_interactive(node):
                legacy_pattern=node.GetLegacyIAccessiblePattern()
                value=legacy_pattern.Value.strip() if legacy_pattern.Value is not None else ""
                name=node.Name.strip()
                element_bounding_box = node.BoundingRectangle
                if is_browser and is_dom:
                    bounding_box=self.iou_bounding_box(self.dom_bounding_box,element_bounding_box)
                    center = bounding_box.get_center()
                    tree_node=TreeElementNode(
                            name=name,
                            control_type=node.LocalizedControlType.title(),
                            value=value,
                            shortcut=node.AcceleratorKey,
                            bounding_box=bounding_box,
                            center=center,
                            xpath=current_xpath,
                            app_name=app_name
                        )
                    dom_interactive_nodes.append(tree_node)
                    dom_correction(node=node)
                else:
                    bounding_box=self.iou_bounding_box(window_bounding_box,element_bounding_box)
                    center = bounding_box.get_center()
                    tree_node=TreeElementNode(
                            name=name,
                            control_type=node.LocalizedControlType.title(),
                            value=value,
                            shortcut=node.AcceleratorKey,
                            bounding_box=bounding_box,
                            center=center,
                            xpath=current_xpath,
                            app_name=app_name
                        )
                    interactive_nodes.append(tree_node)
            elif is_element_text(node):
                informative_nodes.append(TextElementNode(
                    name=node.Name.strip() or "''",
                    app_name=app_name
                ))
            
            children=node.GetChildren()
            type_to_count={}

            # Recursively check all children
            for child in children:
                # Incrementally building the xpath
                control_type=child.ControlTypeName
                if children:
                    type_to_count[control_type]=type_to_count.get(control_type,0)+1
                    child_index=type_to_count[control_type]
                    child_xpath=f'{current_xpath}/{control_type}[{child_index}]'
                else:
                    child_xpath=f'{current_xpath}/{control_type}'
                
                # Check if the child is a DOM element
                if is_browser and child.ClassName == "Chrome_RenderWidgetHostHWND":
                    bounding_box=child.BoundingRectangle
                    self.dom_bounding_box=BoundingBox(left=bounding_box.left,top=bounding_box.top,
                    right=bounding_box.right,bottom=bounding_box.bottom,width=bounding_box.width(),
                    height=bounding_box.height())
                    # enter DOM subtree
                    tree_traversal(child, current_xpath=child_xpath, is_dom=True, is_dialog=is_dialog)
                # Check if the child is a dialog
                elif isinstance(child,WindowControl):
                    if not (is_keyboard_focusable(child) or child.IsOffscreen):
                        if is_dom:
                            bounding_box=child.BoundingRectangle
                            if bounding_box.width() > 0.6*self.screen_box.width:
                                # Because this window element covers the majority of the screen
                                dom_interactive_nodes.clear()
                        else:
                            interactive_nodes.clear()
                        # enter dialog subtree
                        tree_traversal(child, current_xpath=child_xpath, is_dom=is_dom, is_dialog=True)
                else:
                    # normal non-dialog children
                    tree_traversal(child, current_xpath=child_xpath, is_dom=is_dom, is_dialog=is_dialog)

        interactive_nodes, dom_interactive_nodes, informative_nodes, scrollable_nodes = [], [], [],[]
        app_name=node.Name.strip()
        match node.ClassName:
            case "Progman":
                app_name="Desktop"
            case 'Shell_TrayWnd'|'Shell_SecondaryTrayWnd':
                app_name="Taskbar"
            case 'Microsoft.UI.Content.PopupWindowSiteBridge':
                app_name="Context Manager"
            case _:
                pass
        tree_traversal(node,current_xpath=current_xpath,is_dom=False,is_dialog=False)
        interactive_nodes.extend(dom_interactive_nodes)
        return (interactive_nodes,informative_nodes,scrollable_nodes)
    
    def get_random_color(self):
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))

    def annotated_screenshot(self, nodes: list[TreeElementNode],scale:float=0.7) -> Image.Image:
        screenshot = self.desktop.get_screenshot(scale=scale)
        sleep(0.10)
        # Add padding
        padding = 10
        width = screenshot.width + (2 * padding)
        height = screenshot.height + (2 * padding)
        padded_screenshot = Image.new("RGB", (width, height), color=(255, 255, 255))
        padded_screenshot.paste(screenshot, (padding, padding))

        draw = ImageDraw.Draw(padded_screenshot)
        font_size = 12
        try:
            font = ImageFont.truetype('arial.ttf', font_size)
        except IOError:
            font = ImageFont.load_default()

        def get_random_color():
            return "#{:06x}".format(random.randint(0, 0xFFFFFF))

        def draw_annotation(label, node: TreeElementNode):
            box = node.bounding_box
            color = get_random_color()

            # Scale and pad the bounding box also clip the bounding box
            adjusted_box = (
                int(box.left * scale) + padding,
                int(box.top * scale) + padding,
                int(box.right * scale) + padding,
                int(box.bottom * scale) + padding
            )
            # Draw bounding box
            draw.rectangle(adjusted_box, outline=color, width=2)

            # Label dimensions
            label_width = draw.textlength(str(label), font=font)
            label_height = font_size
            left, top, right, bottom = adjusted_box

            # Label position above bounding box
            label_x1 = right - label_width
            label_y1 = top - label_height - 4
            label_x2 = label_x1 + label_width
            label_y2 = label_y1 + label_height + 4

            # Draw label background and text
            draw.rectangle([(label_x1, label_y1), (label_x2, label_y2)], fill=color)
            draw.text((label_x1 + 2, label_y1 + 2), str(label), fill=(255, 255, 255), font=font)

        # Draw annotations in parallel
        with ThreadPoolExecutor() as executor:
            executor.map(draw_annotation, range(len(nodes)), nodes)
        return padded_screenshot
    
    def get_annotated_image_data(self)->tuple[Image.Image,list[TreeElementNode],list[ScrollElementNode]]:
        from uiautomation import GetRootControl
        node=GetRootControl()
        nodes,_,scroll_nodes=self.get_appwise_nodes(node=node)
        screenshot=self.annotated_screenshot(nodes=nodes,scale=1.0)
        return screenshot,nodes,scroll_nodes