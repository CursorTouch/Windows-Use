from uiautomation import GetScreenSize, Control, GetRootControl, ControlType, ControlFromCursor, SetWindowTopmost
from windows_use.desktop.views import DesktopState,App,Size
from windows_use.desktop.config import EXCLUDED_APPS
from PIL.Image import Image as PILImage
from windows_use.tree import Tree
from fuzzywuzzy import process
from screeninfo import get_monitors
from time import sleep
from io import BytesIO
from PIL import Image
import subprocess
import pyautogui
import base64
import csv
import io

class Desktop:
    def __init__(self):
        self.desktop_state=None
        
    def get_state(self,use_vision:bool=False)->DesktopState:
        tree=Tree(self)
        apps=self.get_apps()
        tree_state=tree.get_state()
        active_app,apps=(apps[0],apps[1:]) if len(apps)>0 else (None,[])
        if use_vision:
            monitor_id = self.get_active_monitor(active_app)
            annotated_screenshot=tree.annotated_screenshot(tree_state.interactive_nodes,scale=0.5, monitor_id=monitor_id)
            screenshot=self.screenshot_in_bytes(annotated_screenshot)
        else:
            screenshot=None
        self.desktop_state=DesktopState(apps=apps,active_app=active_app,screenshot=screenshot,tree_state=tree_state)
        return self.desktop_state
    
    def get_taskbar(self)->Control:
        root=GetRootControl()
        taskbar=root.GetFirstChildControl()
        return taskbar
    
    def get_app_status(self,control:Control)->str:
        taskbar=self.get_taskbar()
        taskbar_height=taskbar.BoundingRectangle.height()
        window = control.BoundingRectangle
        screen_width, screen_height = GetScreenSize()
        window_width,window_height=window.width(),window.height()
        if window.isempty():
            return "Minimized"
        if window_width >= screen_width and window_height >= screen_height - taskbar_height:
            return "Maximized"
        return "Normal"
    
    def get_element_under_cursor(self)->Control:
        return ControlFromCursor()
    
    def get_apps_from_start_menu(self)->dict[str,str]:
        command='Get-StartApps | ConvertTo-Csv -NoTypeInformation'
        apps_info,_=self.execute_command(command)
        reader=csv.DictReader(io.StringIO(apps_info))
        return {row.get('Name').lower():row.get('AppID') for row in reader}
    
    def execute_command(self,command:str)->tuple[str,int]:
        try:
            result = subprocess.run(['powershell', '-Command']+command.split(), 
            capture_output=True, check=True)
            return (result.stdout.decode('latin1'),result.returncode)
        except subprocess.CalledProcessError as e:
            return (e.stdout.decode('latin1'),e.returncode)
        
    def launch_app(self,name:str):
        apps_map=self.get_apps_from_start_menu()
        matched_app=process.extractOne(name,apps_map.keys())
        if matched_app is None:
            return (f'Application {name.title()} not found in start menu.',1)
        app_name,_=matched_app
        appid=apps_map.get(app_name)
        if appid is None:
            return (f'Application {name.title()} not found in start menu.',1)
        if name.endswith('.exe'):
            response,status=self.execute_command(f'Start-Process "{appid}"')
        else:
            response,status=self.execute_command(f'Start-Process "shell:AppsFolder\\{appid}"')
        return response,status
    
    def switch_app(self,name:str):
        apps={app.name:app for app in self.desktop_state.apps}
        matched_app:tuple[str,float]=process.extractOne(name,list(apps.keys()))
        if matched_app is None:
            return (f'Application {name.title()} not found.',1)
        app_name,_=matched_app
        app=apps.get(app_name)
        if SetWindowTopmost(app.handle,isTopmost=True):
            return (f'{app_name.title()} switched to foreground.',0)
        else:
            return (f'Failed to switch to {app_name.title()}.',1)
    
    def get_app_size(self,control:Control):
        window=control.BoundingRectangle
        if window.isempty():
            return Size(width=0,height=0)
        return Size(width=window.width(),height=window.height())
    
    def is_app_visible(self,app)->bool:
        is_minimized=self.get_app_status(app)!='Minimized'
        size=self.get_app_size(app)
        area=size.width*size.height
        is_overlay=self.is_overlay_app(app)
        return not is_overlay and is_minimized and area>10
    
    def is_overlay_app(self,element:Control) -> bool:
        no_children = len(element.GetChildren()) == 0
        is_name = "Overlay" in element.Name.strip()
        return no_children or is_name
        
    def get_apps(self) -> list[App]:
        try:
            sleep(1.00)
            desktop = GetRootControl()  # Get the desktop control
            elements = desktop.GetChildren()
            apps = []
            for depth, element in enumerate(elements):
                if element.Name in EXCLUDED_APPS or self.is_overlay_app(element):
                    continue
                if element.ControlType in [ControlType.WindowControl, ControlType.PaneControl]:
                    status = self.get_app_status(element)
                    size=self.get_app_size(element)
                    apps.append(App(name=element.Name, depth=depth, status=status,size=size,handle=element.NativeWindowHandle))
        except Exception as ex:
            print(f"Error: {ex}")
            apps = []
        return apps
    
    def screenshot_in_bytes(self,screenshot:PILImage)->bytes:
        buffer=BytesIO()
        screenshot.save(buffer,format='PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        data_uri = f"data:image/png;base64,{img_base64}"
        return data_uri

    def get_screenshot(self,scale:float=0.7, monitor_id:int=None)->Image.Image:
        if monitor_id is not None:
            monitors = get_monitors()
            if monitor_id < len(monitors):
                monitor = monitors[monitor_id]
                screenshot = pyautogui.screenshot(region=(monitor.x, monitor.y, monitor.width, monitor.height))
            else:
                screenshot = pyautogui.screenshot()
        else:
            screenshot=pyautogui.screenshot()
        size=(screenshot.width*scale, screenshot.height*scale)
        screenshot.thumbnail(size=size, resample=Image.Resampling.LANCZOS)
        return screenshot

    def get_monitors(self):
        return get_monitors()

    def get_active_monitor(self, app: App):
        if app is None:
            return 0 
        monitors = self.get_monitors()
        app_center_x = app.size.width / 2
        for i, monitor in enumerate(monitors):
            if monitor.x <= app_center_x < monitor.x + monitor.width:
                return i
        return 0