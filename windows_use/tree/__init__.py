from windows_use.tree.views import TreeElementNode, TextElementNode, ScrollElementNode, Center, BoundingBox, TreeState
from windows_use.tree.config import INTERACTIVE_CONTROL_TYPE_NAMES,INFORMATIVE_CONTROL_TYPE_NAMES, DEFAULT_ACTIONS
from uiautomation import GetRootControl,Control,ImageControl,ScrollPattern
from windows_use.tree.utils import random_point_within_bounding_box
from concurrent.futures import ThreadPoolExecutor, as_completed
from windows_use.desktop.config import AVOIDED_APPS
from PIL import Image, ImageFont, ImageDraw
from typing import TYPE_CHECKING
from time import sleep
import random

if TYPE_CHECKING:
    from windows_use.desktop import Desktop

class Tree:
    def __init__(self,desktop:'Desktop'):
        self.desktop=desktop

    def get_state(self)->TreeState:
        sleep(0.5)
        # Get the root control of the desktop
        root=GetRootControl()
        interactive_nodes,informative_nodes,scrollable_nodes=self.get_appwise_nodes(node=root)
        return TreeState(interactive_nodes=interactive_nodes,informative_nodes=informative_nodes,scrollable_nodes=scrollable_nodes)
    
    def get_appwise_nodes(self,node:Control) -> tuple[list[TreeElementNode],list[TextElementNode]]:
        all_apps=node.GetChildren()
        visible_apps = [app for app in all_apps if self.desktop.is_app_visible(app) and app.Name not in AVOIDED_APPS]
        interactive_nodes,informative_nodes,scrollable_nodes=[],[],[]
        # Parallel traversal (using ThreadPoolExecutor) to get nodes from each app
        with ThreadPoolExecutor() as executor:
            future_to_node = {executor.submit(self.get_nodes,app,self.desktop.is_app_browser(app)): app for app in visible_apps}
            for future in as_completed(future_to_node):
                try:
                    result = future.result()
                    if result:
                        element_nodes,text_nodes,scroll_nodes=result
                        interactive_nodes.extend(element_nodes)
                        informative_nodes.extend(text_nodes)
                        scrollable_nodes.extend(scroll_nodes)
                except Exception as e:
                    print(f"Error processing node {future_to_node[future].Name}: {e}")
        return interactive_nodes,informative_nodes,scrollable_nodes

    def get_nodes(self, node: Control, is_browser=False) -> tuple[list[TreeElementNode],list[TextElementNode],list[ScrollElementNode]]:
        interactive_nodes, informative_nodes, scrollable_nodes = [], [], []
        app_name=node.Name.strip()
        app_name='Desktop' if node.ClassName=='Progman' else app_name
        
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
                if node.ControlTypeName in INTERACTIVE_CONTROL_TYPE_NAMES:
                    if is_element_visible(node) and is_element_enabled(node) and not is_element_image(node) and is_keyboard_focusable(node):
                        return True
                elif node.ControlTypeName=='GroupControl' and is_browser:
                    if is_element_visible(node) and is_element_enabled(node) and (is_default_action(node) or is_keyboard_focusable(node)):
                        return True
                elif node.ControlTypeName=='GroupControl' and not is_browser:
                    if is_element_visible(node) and is_element_enabled(node) and is_default_action(node):
                        return True
            except Exception:
                return False
            return False
        
        def dom_correction(node:Control):
            if element_has_child_element(node,'list item','link') or element_has_child_element(node,'item','link'):
                interactive_nodes.pop()
                return None
            elif group_has_no_name(node):
                interactive_nodes.pop()
                if is_keyboard_focusable(node):
                    child=node
                    try:
                        while child.GetFirstChildControl() is not None:
                            child=child.GetFirstChildControl()
                    except Exception:
                        return None
                    if child.ControlTypeName!='TextControl':
                        return None
                    control_type='Edit'
                    box = node.BoundingRectangle
                    x,y=box.xcenter(),box.ycenter()
                    center = Center(x=x,y=y)
                    interactive_nodes.append(TreeElementNode(
                        name=child.Name.strip() or "''",
                        control_type=control_type,
                        shortcut=node.AcceleratorKey or "''",
                        bounding_box=BoundingBox(left=box.left,top=box.top,right=box.right,bottom=box.bottom,width=box.width(),height=box.height()),
                        center=center,
                        app_name=app_name
                    ))
            elif element_has_child_element(node,'link','heading'):
                interactive_nodes.pop()
                node=node.GetFirstChildControl()
                control_type='link'
                box = node.BoundingRectangle
                x,y=box.xcenter(),box.ycenter()
                center = Center(x=x,y=y)
                interactive_nodes.append(TreeElementNode(
                    name=node.Name.strip() or "''",
                    control_type=control_type,
                    shortcut=node.AcceleratorKey or "''",
                    bounding_box=BoundingBox(left=box.left,top=box.top,right=box.right,bottom=box.bottom,width=box.width(),height=box.height()),
                    center=center,
                    app_name=app_name
                ))
            
        def tree_traversal(node: Control):
            if is_element_interactive(node):
                box = node.BoundingRectangle
                x,y=random_point_within_bounding_box(node=node,scale_factor=0.5)
                center = Center(x=x,y=y)
                interactive_nodes.append(TreeElementNode(
                    name=node.Name.strip() or "''",
                    control_type=node.LocalizedControlType.title(),
                    shortcut=node.AcceleratorKey or "''",
                    bounding_box=BoundingBox(left=box.left,top=box.top,right=box.right,bottom=box.bottom,width=box.width(),height=box.height()),
                    center=center,
                    app_name=app_name
                ))
                if is_browser:
                    dom_correction(node)
            elif is_element_text(node):
                informative_nodes.append(TextElementNode(
                    name=node.Name.strip() or "''",
                    app_name=app_name
                ))
            elif is_element_scrollable(node):
                scroll_pattern:ScrollPattern=node.GetScrollPattern()
                box = node.BoundingRectangle
                # Get the center
                x,y=random_point_within_bounding_box(node=node,scale_factor=0.8)
                center = Center(x=x,y=y)
                scrollable_nodes.append(ScrollElementNode(
                    name=node.Name.strip() or node.LocalizedControlType.capitalize() or "''",
                    app_name=app_name,
                    control_type=node.LocalizedControlType.title(),
                    bounding_box=BoundingBox(left=box.left,top=box.top,right=box.right,bottom=box.bottom,width=box.width(),height=box.height()),
                    center=center,
                    horizontal_scrollable=scroll_pattern.HorizontallyScrollable,
                    vertical_scrollable=scroll_pattern.VerticallyScrollable
                ))
            # Recursively check all children
            for child in node.GetChildren():
                if child.IsOffscreen and child.ControlTypeName!= 'EditControl' and child.ClassName!="Popup":
                    continue
                tree_traversal(child)
        tree_traversal(node)
        return (interactive_nodes,informative_nodes,scrollable_nodes)
    
    def get_random_color(self):
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))

    def annotated_screenshot(self, nodes: list[TreeElementNode],scale:float=0.7) -> Image.Image:
        screenshot = self.desktop.get_screenshot(scale=scale)
        sleep(0.25)
        # Add padding
        padding = 20
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
    
    def get_annotated_image_data(self)->tuple[Image.Image,list[TreeElementNode]]:
        node=GetRootControl()
        nodes,_,_=self.get_appwise_nodes(node=node)
        screenshot=self.annotated_screenshot(nodes=nodes,scale=1.0)
        return screenshot,nodes