from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, Optional

class SharedBaseModel(BaseModel):

    model_config = ConfigDict(extra='allow')

    thought: str = Field(
        ...,
        description="The rigorous thinking process where you analyze the current state, potential issues, and plan the next steps effectively. (max. 3-5 sentences)"
    )

class App(SharedBaseModel):
    mode: Literal['launch', 'resize', 'switch'] = Field(
        'launch',
        description="Operation mode: 'launch' opens the application from Start Menu, 'resize' adjusts the active window's size and position, 'switch' brings a specific open window into the foreground",
        examples=['launch']
    )
    name: Optional[str] = Field(
        description="Application name as it appears in Start Menu (for launch) or the window title as shown in the taskbar (for switch/resize). Example: 'Notepad' to launch, 'Untitled - Notepad' to switch.",
        examples=['Notepad', 'Google Chrome', 'Untitled - Notepad'],
        default=None
    )
    loc: Optional[list[int]] = Field(
        description="Target [x, y] pixel coordinates for the window's top-left corner. Required for resize mode only.",
        examples=[[0, 0]],
        default=None
    )
    size: Optional[list[int]] = Field(
        description="Target [width, height] in pixels for the window dimensions. Required for resize mode only.",
        examples=[[1920, 1080]],
        default=None
    )

class Done(SharedBaseModel):
    answer: str = Field(
        ...,
        description="The response to deliver to the user, formatted in markdown. This is the ONLY way to communicate with the user.",
        examples=["## Task Completed\n\nThe file has been saved to Desktop.", "Hello! How can I help you today?", "I was unable to find the file. The Downloads folder is empty."]
    )

class Memory(SharedBaseModel):
    mode: Literal['view', 'read', 'write', 'delete', 'update'] = Field(
        description="Operation mode: 'view' lists all stored files, 'read' retrieves file content, 'write' creates a new file, 'update' modifies an existing file, 'delete' removes a file"
    )
    path: Optional[str] = Field(
        None,
        description="Relative file path from the .windows-use/memories directory (e.g., 'notes.md', 'project/data.md'). Required for read, write, update, and delete."
    )
    content: Optional[str] = Field(
        None,
        description="Text content to write into the file. Required for 'write' mode and 'insert' operation in 'update' mode."
    )
    operation: Optional[Literal['replace', 'insert']] = Field(
        'replace',
        description="Update strategy: 'replace' finds old_str and substitutes it with new_str, 'insert' adds content at a specific line number. Only used in 'update' mode."
    )
    old_str: Optional[str] = Field(
        None,
        description="Exact string to find in the file. Required when operation='replace'."
    )
    new_str: Optional[str] = Field(
        None,
        description="Replacement string. Required when operation='replace'."
    )
    line_number: Optional[int] = Field(
        None,
        description="0-indexed line number where content will be inserted. Required when operation='insert'."
    )
    read_range: Optional[list[int]] = Field(
        None,
        description="Optional [start, end] line range for partial reads (0-indexed, end exclusive). Example: [0, 10] reads lines 0 through 9."
    )

class Click(SharedBaseModel):
    loc: list[int] = Field(
        ...,
        description="[x, y] pixel coordinates of the target element to click. Use coordinates from the Interactive Elements list.",
        examples=[[640, 360], [100, 200]]
    )
    button: Literal['left', 'right', 'middle'] = Field(
        description="Mouse button: 'left' for standard clicks and selection, 'right' for context menus, 'middle' for middle-click actions",
        default='left',
        examples=['left', 'right']
    )
    clicks: Literal[0, 1, 2] = Field(
        description="Number of clicks: 1 for single click (select, focus, press buttons), 2 for double click (open files, folders, apps), 0 for hover only (no click performed)",
        default=1,
        examples=[1, 2]
    )

class Shell(SharedBaseModel):
    command: str = Field(
        ...,
        description="PowerShell command to execute. Runs in the user's HOME directory. Use for file operations, system queries, installations, and automation tasks.",
        examples=[
            'Get-Process',
            'ls Desktop',
            'Get-ChildItem -Path C:\\Users -Recurse',
            'echo "Hello World"'
        ]
    )
    timeout: Optional[int] = Field(
        description="Maximum seconds to wait for command completion. Increase for long-running operations.",
        default=10,
        examples=[10, 30, 60]
    )

class Type(SharedBaseModel):
    loc: list[int] = Field(
        ...,
        description="[x, y] pixel coordinates of the input field to type into. The tool clicks this location automatically before typing — do not pre-click.",
        examples=[[640, 360], [200, 150]]
    )
    text: str = Field(
        ...,
        description="The text string to type into the element",
        examples=['hello world', 'user@example.com', 'search query']
    )
    clear: bool = Field(
        description="If true, selects all existing text and replaces it. If false, appends to whatever is already in the field.",
        default=False,
        examples=[True, False]
    )
    caret_position: Literal['start', 'idle', 'end'] = Field(
        description="Where to position the text cursor before typing: 'start' moves to the beginning of the field, 'end' moves to the end, 'idle' leaves it where it is",
        default='idle',
        examples=['start', 'end', 'idle']
    )
    press_enter: bool = Field(
        description="If true, presses Enter after typing to submit the input (search, form, dialog). If false, leaves the cursor in the field.",
        default=False,
        examples=[True, False]
    )

class MultiSelect(SharedBaseModel):
    press_ctrl: bool = Field(
        description="If true, holds Ctrl while clicking each element to accumulate a multi-selection (files, checkboxes, list items). If false, clicks each location sequentially without Ctrl.",
        default=False,
        examples=[True, False]
    )
    elements: list[list[int]] = Field(
        ...,
        description="List of [x, y] pixel coordinates to click. Each coordinate pair is clicked in order.",
        examples=[[[640, 360], [800, 400]], [[100, 200], [200, 300]]]
    )

class MultiEdit(SharedBaseModel):
    elements: list[list] = Field(
        ...,
        description="List of [x, y, text] entries. For each entry, clicks the location (x, y) and types the text. Use to fill multiple form fields in one action.",
        examples=[[[640, 360, 'hello'], [800, 400, 'world']], [[100, 200, 'John'], [200, 300, 'Doe']]]
    )

class Scroll(SharedBaseModel):
    loc: Optional[list[int]] = Field(
        description="[x, y] pixel coordinates where scrolling occurs. If omitted, scrolls at the current cursor position.",
        default=None,
        examples=[[640, 360], [800, 400]]
    )
    type: Literal['horizontal', 'vertical'] = Field(
        description="Scroll axis: 'vertical' for up/down scrolling, 'horizontal' for left/right scrolling",
        default='vertical',
        examples=['vertical', 'horizontal']
    )
    direction: Literal['up', 'down', 'left', 'right'] = Field(
        description="Scroll direction: 'up' or 'down' for vertical, 'left' or 'right' for horizontal",
        default='down',
        examples=['down', 'up', 'right']
    )
    wheel_times: int = Field(
        description="Number of scroll increments. Each increment scrolls roughly 3-5 lines of text. Use 3-5 for moderate scrolling, 10+ for large jumps.",
        default=1,
        examples=[1, 3, 5, 10]
    )

class Move(SharedBaseModel):
    loc: list[int] = Field(
        ...,
        description="[x, y] pixel coordinates to move the mouse cursor to",
        examples=[[640, 360], [100, 100]]
    )
    drag: bool = Field(
        description="If true, holds the left mouse button and drags from the current position to the target (drag-and-drop). If false, moves the cursor without clicking (hover).",
        default=False,
        examples=[True, False]
    )

class Shortcut(SharedBaseModel):
    shortcut: str = Field(
        ...,
        description="Keyboard shortcut to press. Use '+' to combine keys for simultaneous press. Examples: 'ctrl+c' for copy, 'alt+tab' for window switch, 'enter' for confirm, 'escape' for cancel.",
        examples=['enter', 'escape', 'ctrl+c', 'ctrl+v', 'alt+tab', 'ctrl+shift+n', 'win']
    )

class Wait(SharedBaseModel):
    duration: int = Field(
        ...,
        description="Number of seconds to pause. Use to wait for applications to launch, pages to load, or animations to finish before the next action.",
        examples=[2, 5, 10]
    )

class Scrape(SharedBaseModel):
    url: str = Field(
        ...,
        description="URL of the webpage currently open in the browser. The tool extracts visible text content from the rendered page via the accessibility tree and returns it as markdown.",
        examples=['https://google.com', 'https://example.com/page']
    )

class File(SharedBaseModel):
    mode: Literal["read", "write", "list", "delete", "move", "copy", "exists"] = Field(
        ...,
        description="Operation: 'read' retrieves file content, 'write' creates/overwrites a file, 'list' lists directory contents, 'delete' removes a file or directory, 'move' relocates, 'copy' duplicates, 'exists' checks if path exists",
        examples=["read", "write", "list", "delete", "move", "copy", "exists"],
    )
    path: str = Field(
        ...,
        description="Absolute path or path relative to user home directory. Examples: 'C:\\Users\\me\\file.txt', 'Desktop\\notes.txt', 'Documents\\config.json'",
        examples=["C:\\Users\\me\\file.txt", "Desktop\\notes.txt", "Documents\\data.json"],
    )
    destination: Optional[str] = Field(
        None,
        description="Target path for move or copy actions. Required when action is 'move' or 'copy'.",
        examples=["C:\\Users\\me\\backup\\file.txt", "Desktop\\copy.txt"],
    )
    content: Optional[str] = Field(
        None,
        description="Text content to write. Required when action is 'write'.",
        examples=["Hello world", "{\"key\": \"value\"}"],
    )
    encoding: Optional[str] = Field(
        "utf-8",
        description="Character encoding for read and write. Defaults to utf-8.",
        examples=["utf-8", "utf-16", "latin-1"],
    )


class Desktop(SharedBaseModel):
    action: Literal['create', 'remove', 'rename', 'switch'] = Field(
        ...,
        description="Virtual desktop action: 'create' adds a new desktop, 'remove' deletes a desktop by name, 'rename' changes a desktop's name, 'switch' activates a desktop by name",
        examples=['create', 'switch', 'rename', 'remove']
    )
    desktop_name: Optional[str] = Field(
        description="Name of the target desktop. Required for remove, rename, and switch. Optional for create (auto-named if omitted).",
        default=None,
        examples=["Desktop 1", "Work", "Research"]
    )
    new_name: Optional[str] = Field(
        description="New name for the desktop. Required for rename only.",
        default=None,
        examples=["My Workspace", "Project Alpha"]
    )
