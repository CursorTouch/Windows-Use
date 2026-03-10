from typing import Set

# Key name aliases for shortcut keys that differ from UIA SpecialKeyNames
KEY_ALIASES: dict[str, str] = {
    "backspace": "Back",
    "capslock": "Capital",
    "scrolllock": "Scroll",
    "windows": "Win",
    "command": "Win",
    "option": "Alt",
}

AVOIDED_APPS: Set[str] = set([
    'AgentUI'
])

EXCLUDED_APPS:Set[str]=set([
    'Progman',
    'Shell_TrayWnd',
    'Shell_SecondaryTrayWnd',
    'Microsoft.UI.Content.PopupWindowSiteBridge',
    'Windows.UI.Core.CoreWindow',
])