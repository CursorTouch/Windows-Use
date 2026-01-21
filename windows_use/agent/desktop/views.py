from windows_use.agent.tree.views import TreeState,BoundingBox
from dataclasses import dataclass
from tabulate import tabulate
from typing import Optional
from PIL.Image import Image
from enum import Enum

class Browser(Enum):
    CHROME='Chrome'
    EDGE='Edge'
    FIREFOX='Firefox'

class Status(Enum):
    MAXIMIZED='Maximized'
    MINIMIZED='Minimized'
    NORMAL='Normal'
    HIDDEN='Hidden'


@dataclass
class App:
    name:str
    runtime_id:tuple[int]
    is_browser:bool
    depth:int
    status:Status
    bounding_box:BoundingBox
    handle: int
    process_id:int
    
    def to_row(self):
        return [self.name, self.depth, self.status.value, self.bounding_box.width, self.bounding_box.height, self.handle]

@dataclass
class Size:
    width:int
    height:int

    def to_string(self):
        return f'({self.width},{self.height})'

@dataclass
class DesktopState:
    active_desktop:dict
    all_desktops:list[dict]
    apps:list[App]
    active_app:Optional[App]
    screenshot:Optional[Image]=None
    tree_state:Optional[TreeState]=None

    def active_desktop_to_string(self):
        desktop_name=self.active_desktop.get('name')
        desktop_id=self.active_desktop.get('id')
        headers=["Name", "ID"]
        return tabulate([[desktop_name,desktop_id]], headers=headers, tablefmt="simple")

    def desktops_to_string(self):
        headers=["Name", "ID"]
        rows=[[desktop.get("name"),desktop.get("id")] for desktop in self.all_desktops]
        return tabulate(rows, headers=headers, tablefmt="simple")

    def active_app_to_string(self):
        if not self.active_app:
            return 'No active app found'
        headers = ["Name", "Depth", "Status", "Width", "Height", "Handle"]
        return tabulate([self.active_app.to_row()], headers=headers, tablefmt="simple")

    def apps_to_string(self):
        if not self.apps:
            return 'No apps running in background'
        headers = ["Name", "Depth", "Status", "Width", "Height", "Handle"]
        rows = [app.to_row() for app in self.apps]
        return tabulate(rows, headers=headers, tablefmt="simple")