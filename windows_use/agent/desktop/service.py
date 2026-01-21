from windows_use.agent.desktop.config import BROWSER_NAMES, PROCESS_PER_MONITOR_DPI_AWARE
from windows_use.agent.desktop.views import DesktopState, App, Status, Size
from windows_use.agent.tree.views import BoundingBox, TreeElementNode
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import ImageGrab, ImageFont, ImageDraw, Image
from windows_use.agent.tree.service import Tree
from locale import getpreferredencoding
from contextlib import contextmanager
from typing import Optional,Literal
from markdownify import markdownify
from fuzzywuzzy import process
import windows_use.vdm as vdm
from time import sleep,time
from psutil import Process
import win32process
import subprocess
import win32gui
import win32con
import requests
import logging
import base64
import random
import ctypes
import csv
import re
import os
import io

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

try:  
    ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
except Exception:  
    ctypes.windll.user32.SetProcessDPIAware()  

import windows_use.uia as uia
import pyautogui as pg

pg.FAILSAFE=False
pg.PAUSE=1.0

class Desktop:
    def __init__(self):
        self.encoding=getpreferredencoding()
        self.tree=Tree(self)
        self.desktop_state=None
        
    def get_state(self,use_annotation:bool=True,use_vision:bool=False,as_bytes:bool=False)->DesktopState:
        sleep(0.1)
        start_time = time()

        controls_handles=self.get_controls_handles() # Taskbar,Program Manager,Apps, Dialogs
        apps,apps_handles=self.get_apps(controls_handles=controls_handles) # Apps
        active_app=self.get_active_app(apps=apps) #Active App
        active_app_handle=active_app.handle if active_app else None

        if active_app is not None and active_app in apps:
            apps.remove(active_app)

        logger.debug(f"Active app: {active_app or 'No Active App Found'}")
        logger.debug(f"Apps: {apps}")
        
        #Preparing handles for Tree
        other_apps_handles=list(controls_handles-apps_handles)

        tree_state=self.tree.get_state(active_app_handle,other_apps_handles)

        if use_vision:
            if use_annotation:
                nodes=tree_state.interactive_nodes
                screenshot=self.get_annotated_screenshot(nodes=nodes)
            else:
                screenshot=self.get_screenshot()
            if as_bytes:
                buffered = io.BytesIO()
                screenshot.save(buffered, format="PNG")
                screenshot = buffered.getvalue()
                buffered.close()
        else:
            screenshot=None
            
        self.desktop_state=DesktopState(apps= apps,active_app=active_app,screenshot=screenshot,tree_state=tree_state)
        # Log the time taken to capture the state
        end_time = time()
        logger.info(f"Desktop State capture took {end_time - start_time:.2f} seconds")
        return self.desktop_state
    
    def get_app_status(self,control:uia.Control)->Status:
        if uia.IsIconic(control.NativeWindowHandle):
            return Status.MINIMIZED
        elif uia.IsZoomed(control.NativeWindowHandle):
            return Status.MAXIMIZED
        elif uia.IsWindowVisible(control.NativeWindowHandle):
            return Status.NORMAL
        else:
            return Status.HIDDEN
    
    def get_cursor_location(self)->tuple[int,int]:
        position=pg.position()
        return (position.x,position.y)
    
    def get_element_under_cursor(self)->uia.Control:
        return uia.ControlFromCursor()
    
    def get_apps_from_start_menu(self)->dict[str,str]:
        command='Get-StartApps | ConvertTo-Csv -NoTypeInformation'
        apps_info, status = self.execute_command(command)
        
        if status != 0 or not apps_info:
            logger.error(f"Failed to get apps from start menu: {apps_info}")
            return {}

        try:
            reader = csv.DictReader(io.StringIO(apps_info.strip()))
            return {
                row.get('Name').lower(): row.get('AppID') 
                for row in reader 
                if row.get('Name') and row.get('AppID')
            }
        except Exception as e:
            logger.error(f"Error parsing start menu apps: {e}")
            return {}
    
    def execute_command(self,command:str)->tuple[str,int]:
        try:
            encoded = base64.b64encode(command.encode("utf-16le")).decode("ascii")
            result = subprocess.run(
                ['powershell', '-NoProfile', '-EncodedCommand', encoded], 
                capture_output=True, 
                errors='ignore',
                timeout=25,
                cwd=os.path.expanduser(path='~')
            )
            stdout=result.stdout
            stderr=result.stderr
            return (stdout or stderr,result.returncode)
        except subprocess.TimeoutExpired:
            return ('Command execution timed out', 1)
        except Exception as e:
            return ('Command execution failed', 1)
        
    def is_app_browser(self,node:uia.Control):
        '''Give any node of the app and it will return True if the app is a browser, False otherwise.'''
        process=Process(node.ProcessId)
        return process.name() in BROWSER_NAMES
    
    def get_default_language(self)->str:
        command="Get-Culture | Select-Object Name,DisplayName | ConvertTo-Csv -NoTypeInformation"
        response,_=self.execute_command(command)
        reader=csv.DictReader(io.StringIO(response))
        return "".join([row.get('DisplayName') for row in reader])
    
    def resize_app(self,size:tuple[int,int]=None,loc:tuple[int,int]=None)->tuple[str,int]:
        active_app=self.desktop_state.active_app
        if active_app is None:
            return "No active app found",1
        if active_app.status==Status.MINIMIZED:
            return f"{active_app.name} is minimized",1
        elif active_app.status==Status.MAXIMIZED:
            return f"{active_app.name} is maximized",1
        else:
            app_control=uia.ControlFromHandle(active_app.handle)
            if loc is None:
                x=app_control.BoundingRectangle.left
                y=app_control.BoundingRectangle.top
                loc=(x,y)
            if size is None:
                width=app_control.BoundingRectangle.width()
                height=app_control.BoundingRectangle.height()
                size=(width,height)
            x,y=loc
            width,height=size
            app_control.MoveWindow(x,y,width,height)
            return (f'{active_app.name} resized to {width}x{height} at {x},{y}.',0)
    
    def is_app_running(self,name:str)->bool:
        apps, _ = self.get_apps()
        apps_dict = {app.name: app for app in apps}
        return process.extractOne(name,list(apps_dict.keys()),score_cutoff=60) is not None
    
    def app(self,mode:Literal['launch','switch','resize'],name:Optional[str]=None,loc:Optional[tuple[int,int]]=None,size:Optional[tuple[int,int]]=None):
        match mode:
            case 'launch':
                response,status,pid=self.launch_app(name)
                if status!=0:
                    return response
                
                # Smart wait using UIA Exists (avoids manual Python loops)
                launched = False
                if pid > 0:
                    if uia.WindowControl(ProcessId=pid).Exists(maxSearchSeconds=10):
                        launched = True
                
                if not launched:
                    # Fallback: Regex search for the window title
                    safe_name = re.escape(name)
                    if uia.WindowControl(RegexName=f'(?i).*{safe_name}.*').Exists(maxSearchSeconds=10):
                        launched = True

                if launched:
                    return f'{name.title()} launched.'
                return f'Launching {name.title()} sent, but window not detected yet.'
            case 'resize':
                response,status=self.resize_app(size=size,loc=loc)
                if status!=0:
                    return response
                else:
                    return response
            case 'switch':
                response,status=self.switch_app(name)
                if status!=0:
                    return response
                else:
                    return response
        
    def launch_app(self,name:str)->tuple[str,int,int]:
        apps_map=self.get_apps_from_start_menu()
        matched_app=process.extractOne(name,apps_map.keys(),score_cutoff=70)
        if matched_app is None:
            return (f'{name.title()} not found in start menu.',1,0)
        app_name,_=matched_app
        appid=apps_map.get(app_name)
        if appid is None:
            return (name,f'{name.title()} not found in start menu.',1,0)
        
        pid = 0
        if os.path.exists(appid) or "\\" in appid:
            # It's a file path, we can try to get the PID using PassThru
            command = f'Start-Process "{appid}" -PassThru | Select-Object -ExpandProperty Id'
            response, status = self.execute_command(command)
            if status == 0 and response.strip().isdigit():
                pid = int(response.strip())
        else:
            # It's an AUMID (Store App)
            command = f'Start-Process "shell:AppsFolder\\{appid}"'
            response, status = self.execute_command(command)
            
        return response, status, pid
    
    def switch_app(self,name:str):
        apps={app.name:app for app in [self.desktop_state.active_app]+self.desktop_state.apps if app is not None}
        matched_app:Optional[tuple[str,float]]=process.extractOne(name,list(apps.keys()),score_cutoff=70)
        if matched_app is None:
            return (f'Application {name.title()} not found.',1)
        app_name,_=matched_app
        app=apps.get(app_name)
        target_handle=app.handle

        if uia.IsIconic(target_handle):
            uia.ShowWindow(target_handle, win32con.SW_RESTORE)
            content=f'{app_name.title()} restored from Minimized state.'
        else:
            self.bring_window_to_top(target_handle)
            content=f'Switched to {app_name.title()} window.'
        return content,0
    
    def bring_window_to_top(self,target_handle:int):
        foreground_handle=win32gui.GetForegroundWindow()
        foreground_thread,_=win32process.GetWindowThreadProcessId(foreground_handle)
        target_thread,_=win32process.GetWindowThreadProcessId(target_handle)
        try:
            ctypes.windll.user32.AllowSetForegroundWindow(-1)
            win32process.AttachThreadInput(foreground_thread,target_thread,True)
            win32gui.SetForegroundWindow(target_handle)
            win32gui.BringWindowToTop(target_handle)
        except Exception as e:
            logger.error(f'Failed to bring window to top: {e}')
        finally:
            win32process.AttachThreadInput(foreground_thread,target_thread,False)
    
    def get_element_handle_from_label(self,label:int)->uia.Control:
        tree_state=self.desktop_state.tree_state
        element_node=tree_state.interactive_nodes[label]
        xpath=element_node.xpath
        element_handle=self.get_element_from_xpath(xpath)
        return element_handle
    
    def get_coordinates_from_label(self,label:int)->tuple[int,int]:
        element_handle=self.get_element_handle_from_label(label)
        bounding_rectangle=element_handle.BoundingRectangle
        return bounding_rectangle.xcenter(),bounding_rectangle.ycenter()
        
    def click(self,loc:tuple[int,int],button:str='left',clicks:int=2):
        x,y=loc
        pg.click(x,y,button=button,clicks=clicks,duration=0.1)

    def type(self,loc:tuple[int,int],text:str,caret_position:Literal['start','end','none']='none',clear:Literal['true','false']='false',press_enter:Literal['true','false']='false'):
        x,y=loc
        pg.leftClick(x,y)
        if caret_position == 'start':
            pg.press('home')
        elif caret_position == 'end':
            pg.press('end')
        else:
            pass
        if clear=='true':
            pg.sleep(0.5)
            pg.hotkey('ctrl','a')
            pg.press('backspace')
        pg.typewrite(text,interval=0.02)
        if press_enter=='true':
            pg.press('enter')

    def scroll(self,loc:tuple[int,int]=None,type:Literal['horizontal','vertical']='vertical',direction:Literal['up','down','left','right']='down',wheel_times:int=1)->str|None:
        if loc:
            self.move(loc)
        match type:
            case 'vertical':
                match direction:
                    case 'up':
                        uia.WheelUp(wheel_times)
                    case 'down':
                        uia.WheelDown(wheel_times)
                    case _:
                        return 'Invalid direction. Use "up" or "down".'
            case 'horizontal':
                match direction:
                    case 'left':
                        pg.keyDown('Shift')
                        pg.sleep(0.05)
                        uia.WheelUp(wheel_times)
                        pg.sleep(0.05)
                        pg.keyUp('Shift')
                    case 'right':
                        pg.keyDown('Shift')
                        pg.sleep(0.05)
                        uia.WheelDown(wheel_times)
                        pg.sleep(0.05)
                        pg.keyUp('Shift')
                    case _:
                        return 'Invalid direction. Use "left" or "right".'
            case _:
                return 'Invalid type. Use "horizontal" or "vertical".'
        return None
    
    def drag(self,loc:tuple[int,int]):
        x,y=loc
        pg.sleep(0.5)
        pg.dragTo(x,y,duration=0.6)

    def move(self,loc:tuple[int,int]):
        x,y=loc
        pg.moveTo(x,y,duration=0.1)

    def shortcut(self,shortcut:str):
        shortcut=shortcut.split('+')
        if len(shortcut)>1:
            pg.hotkey(*shortcut)
        else:
            pg.press(''.join(shortcut))

    def multi_select(self,press_ctrl:Literal['true','false']='false',elements:list[tuple[int,int]|int]=[]):
        if press_ctrl=='true':
            pg.keyDown('ctrl')
        for element in elements:
            x,y=element
            pg.click(x,y,duration=0.2)
            pg.sleep(0.5)
        pg.keyUp('ctrl')
    
    def multi_edit(self,elements:list[tuple[int,int,str]|tuple[int,str]]):
        for element in elements:
            x,y,text=element
            self.type((x,y),text=text,clear='true')
    
    def scrape(self,url:str)->str:
        response=requests.get(url,timeout=10)
        html=response.text
        content=markdownify(html=html)
        return content
    
    def get_app_from_element(self,element:uia.Control)->App|None:
        if element is None:
            return None
        top_window=element.GetTopLevelControl()
        if top_window is None:
            return None
        handle=top_window.NativeWindowHandle
        apps,_=self.get_apps()
        for app in apps:
            if app.handle==handle:
                return app
        return None
    
    def is_app_visible(self,app:uia.Control)->bool:
        is_minimized=self.get_app_status(app)!=Status.MINIMIZED
        size=app.BoundingRectangle
        area=size.width()*size.height()
        is_overlay=self.is_overlay_app(app)
        return not is_overlay and is_minimized and area>10
    
    def is_overlay_app(self,element:uia.Control) -> bool:
        no_children = len(element.GetChildren()) == 0
        is_name = "Overlay" in element.Name.strip()
        return no_children or is_name

    def get_controls_handles(self,optimized:bool=False):
        handles = set()
        if optimized:
            # For even more faster results (still under development)
            def callback(hwnd, _):
                if win32gui.IsWindowVisible(hwnd) and vdm.is_window_on_current_desktop(hwnd):
                    handles.add(hwnd)
            win32gui.EnumWindows(callback, None)

            if desktop_hwnd:= win32gui.FindWindow('Progman',None):
                handles.add(desktop_hwnd)
            if taskbar_hwnd:= win32gui.FindWindow('Shell_TrayWnd',None):
                handles.add(taskbar_hwnd)
            if secondary_taskbar_hwnd:= win32gui.FindWindow('Shell_SecondaryTrayWnd',None):
                handles.add(secondary_taskbar_hwnd)
            if start_hwnd:= win32gui.FindWindow('Windows.UI.Core.CoreWindow','Start'):
                handles.add(start_hwnd)
            if search_hwnd:= win32gui.FindWindow('Windows.UI.Core.CoreWindow','Search'):
                handles.add(search_hwnd)
        else:
            root=uia.GetRootControl()
            children=root.GetChildren()
            for child in children:
                handles.add(child.NativeWindowHandle)
        return handles

    def get_active_app(self,apps:list[App]|None=None)->App|None:
        try:
            if apps is None:
                apps,_=self.get_apps()
            handle=uia.GetForegroundWindow()
            for app in apps:
                if app.handle!=handle:
                    continue
                return app
        except Exception as ex:
            logger.error(f"Error in get_active_app: {ex}")
        return None
        
    def get_apps(self,controls_handles:set[int]|None=None) -> tuple[list[App],set[int]]:
        try:
            apps = []
            handles = set()
            controls_handles=controls_handles or self.get_controls_handles()
            for depth, hwnd in enumerate(controls_handles):
                try:
                    child = uia.ControlFromHandle(hwnd)
                except Exception:
                    continue
                
                # Filter out Overlays (e.g. NVIDIA, Steam)
                if self.is_overlay_app(child):
                    continue

                if isinstance(child,(uia.WindowControl,uia.PaneControl)):
                    window_pattern=child.GetPattern(uia.PatternId.WindowPattern)
                    if (window_pattern is None):
                        continue
                        
                    if window_pattern.CanMinimize and window_pattern.CanMaximize:
                        status = self.get_app_status(child)
                        
                        bounding_rect=child.BoundingRectangle
                        if bounding_rect.isempty() and status!=Status.MINIMIZED:
                            continue

                        apps.append(App(**{
                            "name":child.Name,
                            "runtime_id":tuple(child.GetRuntimeId()),
                            "depth":depth,
                            "status":status,
                            "bounding_box":BoundingBox(
                                left=bounding_rect.left,
                                top=bounding_rect.top,
                                right=bounding_rect.right,
                                bottom=bounding_rect.bottom,
                                width=bounding_rect.width(),
                                height=bounding_rect.height()
                            ),
                            "handle":child.NativeWindowHandle,
                            "process_id":child.ProcessId,
                            "is_browser":self.is_app_browser(child)
                        }))
                        handles.add(child.NativeWindowHandle)
        except Exception as ex:
            logger.error(f"Error in get_apps: {ex}")
            apps = []
        return apps,handles
    
    def get_xpath_from_element(self,element:uia.Control):
        current=element
        if current is None:
            return ""
        path_parts=[]
        while current is not None:
            parent=current.GetParentControl()
            if parent is None:
                # we are at the root node
                path_parts.append(f'{current.ControlTypeName}')
                break
            children=parent.GetChildren()
            same_type_children=["-".join(map(lambda x:str(x),child.GetRuntimeId())) for child in children if child.ControlType==current.ControlType]
            index=same_type_children.index("-".join(map(lambda x:str(x),current.GetRuntimeId())))
            if same_type_children:
                path_parts.append(f'{current.ControlTypeName}[{index+1}]')
            else:
                path_parts.append(f'{current.ControlTypeName}')
            current=parent
        path_parts.reverse()
        xpath="/".join(path_parts)
        return xpath

    def get_element_from_xpath(self,xpath:str)->uia.Control:
        pattern = re.compile(r'(\w+)(?:\[(\d+)\])?')
        parts=xpath.split("/")
        root=uia.GetRootControl()
        element=root
        for part in parts[1:]:
            match=pattern.fullmatch(part)
            if match is None:
                continue
            control_type, index=match.groups()
            index=int(index) if index else None
            children=element.GetChildren()
            same_type_children=list(filter(lambda x:x.ControlTypeName==control_type,children))
            if index:
                element=same_type_children[index-1]
            else:
                element=same_type_children[0]
        return element
    
    def get_windows_version(self)->str:
        response,status=self.execute_command("(Get-CimInstance Win32_OperatingSystem).Caption")
        if status==0:
            return response.strip()
        return "Windows"
    
    def get_user_account_type(self)->str:
        response,status=self.execute_command("(Get-LocalUser -Name $env:USERNAME).PrincipalSource")
        return "Local Account" if response.strip()=='Local' else "Microsoft Account" if status==0 else "Local Account"
    
    def get_dpi_scaling(self):
        user32 = ctypes.windll.user32
        dpi = user32.GetDpiForSystem()
        return dpi / 96.0
    
    def get_screen_size(self)->Size:
        width, height = uia.GetVirtualScreenSize()
        return Size(width=width,height=height)

    def get_screenshot(self)->Image.Image:
        try:
            return ImageGrab.grab(all_screens=True)
        except Exception as e:
            logger.warning(f"Failed to capture virtual screen, using primary screen")
            return pg.screenshot()

    def get_annotated_screenshot(self, nodes: list[TreeElementNode]) -> Image.Image:
        screenshot = self.get_screenshot()
        sleep(0.10)
        # Add padding
        padding = 5
        width = int(screenshot.width + (1.5 * padding))
        height = int(screenshot.height + (1.5 * padding))
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

        left_offset, top_offset, _, _ = uia.GetVirtualScreenRect()

        def draw_annotation(label, node: TreeElementNode):
            box = node.bounding_box
            color = get_random_color()

            # Scale and pad the bounding box also clip the bounding box
            # Adjust for virtual screen offset so coordinates map to the screenshot image
            adjusted_box = (
                int(box.left - left_offset) + padding,
                int(box.top - top_offset) + padding,
                int(box.right - left_offset) + padding,
                int(box.bottom - top_offset) + padding
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
    
    @contextmanager
    def auto_minimize(self):
        try:
            handle = uia.GetForegroundWindow()
            uia.ShowWindow(handle, win32con.SW_MINIMIZE)
            yield
        finally:
            uia.ShowWindow(handle, win32con.SW_RESTORE)