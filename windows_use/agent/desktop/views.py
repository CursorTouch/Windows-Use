from windows_use.agent.tree.views import TreeState
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
    depth:int
    status:Status
    size:'Size'
    handle: int
    
    def to_row(self):
        return [self.name, self.depth, self.status.value, self.size.width, self.size.height, self.handle]

@dataclass
class Size:
    width:int
    height:int

    def to_string(self):
        return f'({self.width},{self.height})'

@dataclass
class DesktopState:
    apps:list[App]
    active_app:Optional[App]
    screenshot:Image|None
    tree_state:TreeState

    def active_app_to_string(self):
        if self.active_app is None:
            return 'No active app found'
        headers = ["Name", "Depth", "Status", "Width", "Height", "Handle"]
        return tabulate([self.active_app.to_row()], headers=headers, tablefmt="github")

    def apps_to_string(self):
        if not self.apps:
            return 'No apps running in background'
        headers = ["Name", "Depth", "Status", "Width", "Height", "Handle"]
        rows = [app.to_row() for app in self.apps]
        return tabulate(rows, headers=headers, tablefmt="github")