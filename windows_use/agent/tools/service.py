from windows_use.agent.tools.views import Click, Type, Scroll, Move, Shortcut, Wait, Scrape, Done, Shell, Memory, App, MultiSelect, MultiEdit, Desktop, File
from windows_use.vdm.core import create_desktop as vdm_create, remove_desktop as vdm_remove, rename_desktop as vdm_rename, switch_desktop as vdm_switch
from windows_use.agent.desktop.service import Desktop as _Desktop
from windows_use.tools import Tool
from typing import Literal,Optional
from datetime import datetime
from pathlib import Path
from time import sleep
import shutil

MAX_FILE_READ_SIZE = 1 * 1024 * 1024  # 1 MB


def _format_size(size: int) -> str:
    """Format size in human-readable form."""
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024:
            return f"{size} {unit}"
        size /= 1024
    return f"{size:.1f} PB"

WINDOWS_USE_DIR = Path.home() / ".windows-use"
memory_path = WINDOWS_USE_DIR / "memory"
memory_path.mkdir(parents=True, exist_ok=True)

def _resolve_memory_path(path: str) -> Path:
    """Resolve a memory file path, always sandboxed within .windows-use/memories directory."""
    file_path = (memory_path / path).resolve()
    if not str(file_path).startswith(str(memory_path.resolve())):
        raise ValueError(f"Path escapes the .windows-use/memories directory: {path}")
    return file_path

@Tool('done_tool',model=Done)
async def done_tool(answer:str,**kwargs):
    '''
    Delivers a response to the user. This is the ONLY way to communicate with the user.

    MUST be called for every type of response:
    - Task completion: summarize what was accomplished
    - Answers to questions: provide the requested information
    - Conversational replies: greetings, clarifications, explanations
    - Error reports: explain what failed and why

    The answer should be formatted in clean markdown.
    '''
    return answer

@Tool('app_tool',model=App)
async def app_tool(mode:Literal['launch','resize','switch']='launch',name:Optional[str]=None,loc:Optional[list[int]]=None,size:Optional[list[int]]=None,**kwargs)->str:
    '''
    Manages application windows: launch new apps, switch between open windows, or resize/reposition the active window.

    - launch: Opens an application via the Start Menu. Provide the app name as it appears in Start Menu.
    - switch: Brings an already-open window to the foreground. Provide the window title from the Window Info list.
    - resize: Moves and resizes the currently active window. Provide loc=[x,y] for position and size=[w,h] for dimensions.
    '''
    desktop:_Desktop=kwargs['desktop']
    return desktop.app(mode,name,loc,size)



@Tool('memory_tool', model=Memory)
async def memory_tool(mode: Literal['view', 'read', 'write', 'delete', 'update'], path: Optional[str] = None,
    content: Optional[str] = None, operation: Optional[Literal['replace', 'insert']] = 'replace',
    old_str: Optional[str] = None, new_str: Optional[str] = None, line_number: Optional[int] = None,
    read_range: Optional[list[int]] = None, **kwargs) -> str:
    '''
    Persistent file-based storage for saving and retrieving information across steps. Files are stored as markdown in the .windows-use/memories directory (user home).

    - view: List all stored memory files. Optionally provide a subdirectory path to list only files within it.
    - write: Create a new file. Requires path and content. Path must end with .md extension.
    - read: Retrieve file contents. Optionally use read_range=[start, end] for partial reads.
    - update: Modify an existing file. Use operation='replace' with old_str/new_str, or operation='insert' with line_number/content.
    - delete: Remove a file by path.

    Use for storing intermediate results, research findings, plans, or any data needed in later steps.
    '''
    match mode:
        case 'view':
            search_dir = (memory_path / path).resolve() if path else memory_path
            if not str(search_dir).startswith(str(memory_path.resolve())):
                return "Error: path escapes the .windows-use/memories directory."
            if not search_dir.exists():
                return "No memory files found."
            files = search_dir.rglob('*.md')
            result = '\n'.join([f'{i + 1}. {file.relative_to(memory_path).as_posix()}'
                               for i, file in enumerate(files)])
            return result if result else "No memory files found."

        case 'write':
            if not path:
                return "Error: path is required for write mode."
            if not path.endswith('.md'):
                path += '.md'
            file_path = _resolve_memory_path(path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding='utf-8')
            return f'{file_path.name} created in {file_path.parent.relative_to(memory_path).as_posix()}.'

        case 'read':
            if not path:
                return "Error: path is required for read mode."
            file_path = _resolve_memory_path(path)
            if not file_path.exists():
                return f'Error: {file_path.name} not found.'

            file_content = file_path.read_text(encoding='utf-8')

            if read_range:
                start, end = read_range
                lines = file_content.splitlines()

                if start < 0 or start >= len(lines):
                    return f'Error: start line {start} out of range (0-{len(lines) - 1}).'
                if end < start or end > len(lines):
                    return f'Error: end line {end} out of range ({start}-{len(lines)}).'

                selected_lines = lines[start:end]
                return f"File: {file_path.relative_to(memory_path).as_posix()}\nLines {start}-{end - 1}:\n" + '\n'.join(selected_lines)

            return f"File: {file_path.relative_to(memory_path).as_posix()}\nContent:\n{file_content}"

        case 'update':
            if not path:
                return "Error: path is required for update mode."
            file_path = _resolve_memory_path(path)
            if not file_path.exists():
                return f'Error: {file_path.name} not found. Use "write" mode to create a new file.'

            current_content = file_path.read_text(encoding='utf-8')

            match operation:
                case 'replace':
                    if not old_str or not new_str:
                        return 'Error: both old_str and new_str are required for replace operation.'
                    if old_str not in current_content:
                        return f'Error: "{old_str}" not found in file.'

                    new_content = current_content.replace(old_str, new_str)
                    file_path.write_text(new_content, encoding='utf-8')
                    old_display = f'"{old_str[:50]}{"..." if len(old_str) > 50 else ""}"'
                    new_display = f'"{new_str[:50]}{"..." if len(new_str) > 50 else ""}"'
                    return f'{file_path.name} updated: replaced {old_display} with {new_display}.'

                case 'insert':
                    if line_number is None:
                        return 'Error: line_number is required for insert operation.'
                    if not content:
                        return 'Error: content is required for insert operation.'

                    lines = current_content.splitlines(keepends=True)
                    if line_number < 0 or line_number > len(lines):
                        return f'Error: line_number {line_number} out of range (0-{len(lines)}).'

                    lines.insert(line_number, content + '\n' if not content.endswith('\n') else content)
                    new_content = ''.join(lines)
                    file_path.write_text(new_content, encoding='utf-8')
                    return f'{file_path.name} updated: inserted content at line {line_number}.'

                case _:
                    return f'Error: Unknown operation "{operation}".'

        case 'delete':
            if not path:
                return "Error: path is required for delete mode."
            file_path = _resolve_memory_path(path)
            if not file_path.exists():
                return f'Error: {file_path.name} not found.'

            file_path.unlink()
            return f'{file_path.name} deleted from {file_path.parent.relative_to(memory_path).as_posix()}.'

    return "Invalid mode. Use 'view', 'write', 'read', 'update', or 'delete'."


def _resolve_file_path(path: str) -> Path:
    """Resolve a file path. Relative paths are resolved against user home. Rejects null bytes."""
    if "\x00" in path:
        raise ValueError("Path contains null byte")
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = Path.home() / p
    return p.resolve()


@Tool("file_tool", model=File)
async def file_tool(
    mode: Literal["read", "write", "list", "delete", "move", "copy", "exists"],
    path: str,
    destination: Optional[str] = None,
    content: Optional[str] = None,
    encoding: str = "utf-8",
    **kwargs,
) -> str:
    '''
    Performs file system operations: read, write, list, delete, move, copy, or check existence.

    - read: Returns file content. Paths are relative to user home directory or absolute.
    - write: Creates or overwrites a file. Requires content.
    - list: Lists directory contents (files and subdirectories).
    - delete: Removes a file or empty directory.
    - move: Moves a file or directory to destination.
    - copy: Copies a file to destination.
    - exists: Returns whether the path exists.

    Use for reading config files, writing outputs, organizing files, or checking file presence.
    '''
    try:
        resolved = _resolve_file_path(path)
    except ValueError as e:
        return f"Error: {e}"

    match mode:
        case "read":
            if not resolved.exists():
                return f"Error: Path does not exist: {path}"
            if resolved.is_dir():
                return f"Error: Cannot read directory as file: {path}"
            try:
                size = resolved.stat().st_size
                if size > MAX_FILE_READ_SIZE:
                    return f"Error: File too large to read ({size} bytes, max {MAX_FILE_READ_SIZE})."
                text = resolved.read_text(encoding=encoding)
                return f"File: {resolved}\nContent:\n{text}"
            except UnicodeDecodeError as e:
                return f"Error: Could not decode file ({encoding}): {e}"
            except OSError as e:
                return f"Error reading file: {e}"

        case "write":
            if content is None:
                return "Error: content is required for write action."
            try:
                resolved.parent.mkdir(parents=True, exist_ok=True)
                resolved.write_text(content, encoding=encoding)
                return f"Wrote {len(content)} characters to {resolved}."
            except OSError as e:
                return f"Error writing file: {e}"

        case "list":
            if not resolved.exists():
                return f"Error: Path does not exist: {path}"
            if not resolved.is_dir():
                return f"Error: Not a directory: {path}"
            try:
                entries = sorted(resolved.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
                lines = []
                for e in entries:
                    try:
                        stat = e.stat()
                        mtime = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
                        size = stat.st_size if e.is_file() else 0
                        size_str = _format_size(size)
                        kind = "d" if e.is_dir() else "-"
                        lines.append(f"{kind}  {mtime}  {size_str:>10}  {e.name}")
                    except OSError:
                        lines.append(f"?  {'?':>19}  {'?':>10}  {e.name}")
                header = f"{'Type':<4} {'Modified':<17} {'Size':>10}  Name"
                return f"Directory: {resolved}\n\n{header}\n{'-' * 45}\n" + "\n".join(lines)
            except OSError as e:
                return f"Error listing directory: {e}"

        case "delete":
            if not resolved.exists():
                return f"Error: Path does not exist: {path}"
            try:
                if resolved.is_dir():
                    resolved.rmdir()
                    return f"Removed directory: {resolved}"
                resolved.unlink()
                return f"Deleted file: {resolved}"
            except OSError as e:
                return f"Error deleting: {e}"

        case "move":
            if not destination:
                return "Error: destination is required for move action."
            try:
                dest = _resolve_file_path(destination)
                shutil.move(str(resolved), str(dest))
                return f"Moved {resolved} to {dest}."
            except ValueError as e:
                return f"Error: {e}"
            except OSError as e:
                return f"Error moving: {e}"

        case "copy":
            if not destination:
                return "Error: destination is required for copy action."
            if resolved.is_dir():
                return f"Error: copy does not support directories. Use move for directories."
            try:
                dest = _resolve_file_path(destination)
                shutil.copy2(str(resolved), str(dest))
                return f"Copied {resolved} to {dest}."
            except ValueError as e:
                return f"Error: {e}"
            except OSError as e:
                return f"Error copying: {e}"

        case "exists":
            return f"Path exists: {resolved.exists()}"

    return f"Error: Unknown action '{action}'."


@Tool('shell_tool',model=Shell)
async def shell_tool(command: str,timeout:int=10,**kwargs) -> str:
    '''
    Executes a PowerShell command and returns the output and exit status code. Working directory is the user's HOME.

    Use for file operations, system queries, installations, running scripts, and any task better done via command line than GUI. Check the status code in the response: 0 means success, non-zero means failure.
    '''
    desktop:_Desktop=kwargs['desktop']
    response,status=desktop.execute_command(command,timeout=timeout)
    return f'Response: {response}\nStatus Code: {status}'

@Tool('click_tool',model=Click)
async def click_tool(loc:Optional[list[int]]=None,button:Literal['left','right','middle']='left',clicks:int=1,**kwargs)->str:
    '''
    Clicks at the specified pixel coordinates on screen.

    - Single left click (clicks=1): Select elements, press buttons, focus fields, follow links.
    - Double left click (clicks=2): Open files, folders, and desktop icons.
    - Right click (button='right'): Open context menus.
    - Hover only (clicks=0): Move cursor to location without clicking.

    Use coordinates from the Interactive Elements list in the Desktop State.
    '''
    x,y=loc
    desktop:_Desktop=kwargs['desktop']
    desktop.click(loc,button,clicks)
    num_clicks={1:'Single',2:'Double',3:'Triple'}
    return f'{num_clicks.get(clicks)} {button} clicked at ({x},{y}).'

@Tool('type_tool',model=Type)
async def type_tool(loc:Optional[list[int]]=None,text:str='',clear:Literal['true','false']='false',caret_position:Literal['start','idle','end']='idle',press_enter:Literal['true','false']='false',**kwargs):
    '''
    Clicks an input field and types text into it. Do NOT pre-click with click_tool — this tool handles focusing automatically.

    - Set clear=true to replace existing text, or clear=false to append.
    - Set press_enter=true to submit after typing (search bars, forms, dialogs).
    - Set caret_position to control where typing begins relative to existing text.

    Use for search queries, form fields, text editors, address bars, and any text input.
    '''
    x,y=loc
    desktop:_Desktop=kwargs['desktop']
    desktop.type(loc=loc,text=text,caret_position=caret_position,clear=clear,press_enter=press_enter)
    return f'Typed {text} at ({x},{y}).'

@Tool('scroll_tool',model=Scroll)
async def scroll_tool(loc:Optional[list[int]]=None,type:Literal['horizontal','vertical']='vertical',direction:Literal['up','down','left','right']='down',wheel_times:int=1,**kwargs)->str:
    '''
    Scrolls content at the specified location or at the current cursor position.

    Each wheel increment scrolls roughly 3-5 lines of text. Use wheel_times=3-5 for moderate scrolling, 10+ for large jumps.

    Check scroll percentages in the Scrollable Elements list to gauge position before scrolling. If loc is omitted, scrolling occurs at the current cursor location.
    '''
    desktop:_Desktop=kwargs['desktop']
    response=desktop.scroll(loc,type,direction,wheel_times)
    if response:
        return response
    return f'Scrolled {type} {direction} by {wheel_times} wheel times.'

@Tool('move_tool',model=Move)
async def move_tool(loc:list[int],drag:bool=False,**kwargs)->str:
    '''
    Moves the mouse cursor to a target location, or drags from the current position to the target.

    - drag=false: Hover over elements to reveal tooltips, dropdown menus, or reposition the cursor.
    - drag=true: Hold left mouse button from the current cursor position and drag to the target coordinates. Use for drag-and-drop of files, window resizing, slider adjustment, or reordering items.
    '''
    x,y=loc
    desktop:_Desktop=kwargs['desktop']
    if drag:
        desktop.drag(loc)
        return f'Dragged the selected element to ({x},{y}).'
    else:
        desktop.move(loc)
        return f'Moved the mouse pointer to ({x},{y}).'

@Tool('shortcut_tool',model=Shortcut)
async def shortcut_tool(shortcut:str,**kwargs)->str:
    '''
    Presses a keyboard shortcut. Use '+' to combine keys (e.g., 'ctrl+c').

    Common shortcuts: ctrl+c (copy), ctrl+v (paste), ctrl+z (undo), ctrl+s (save), ctrl+a (select all), ctrl+f (find), ctrl+w (close tab), ctrl+t (new tab), alt+tab (switch window), alt+f4 (close app), enter (confirm), escape (cancel), win (start menu).

    Prefer shortcuts over mouse interactions when the operation is unambiguous.
    '''
    desktop:_Desktop=kwargs['desktop']
    desktop.shortcut(shortcut)
    return f'Pressed {shortcut}.'

@Tool('multi_select_tool',model=MultiSelect)
async def multi_select_tool(press_ctrl:Literal['true','false']='true',elements:list[list[int]]=[],**kwargs)->str:
    '''
    Clicks multiple locations in sequence. With press_ctrl=true, holds Ctrl to accumulate a multi-selection (e.g., selecting multiple files, checkboxes, or list items). With press_ctrl=false, clicks each location independently in order.

    Provide a list of [x, y] coordinates. Each is clicked once in the order given.
    '''
    desktop:_Desktop=kwargs['desktop']
    desktop.multi_select(press_ctrl,elements)
    elements_str = '\n'.join([f"({x},{y})" for x,y in elements])
    return f'Multi-selected elements at {elements_str}.'

@Tool('multi_edit_tool',model=MultiEdit)
async def multi_edit_tool(elements:list[list],**kwargs)->str:
    '''
    Types text into multiple input fields in one action. Each entry is [x, y, text]: the tool clicks the location and types the text, then moves to the next entry.

    Use for filling out forms with multiple fields (name, email, address) or editing several text inputs at once. More efficient than calling type_tool repeatedly.
    '''
    desktop:_Desktop=kwargs['desktop']
    desktop.multi_edit(elements)
    elements_str = ','.join([f'({x},{y}) text={text}' for x,y,text in elements])
    return f'Multi-edited elements at {elements_str}.'

@Tool('wait_tool',model=Wait)
async def wait_tool(duration:int,**kwargs)->str:
    '''
    Pauses for the specified number of seconds before the next action. Use to wait for applications to launch, pages to load, dialogs to appear, or animations to finish. Typical waits: 2-3s for UI transitions, 5s for app launches, 10s+ for installations or downloads.
    '''
    import asyncio
    await asyncio.sleep(duration)
    return f'Waited for {duration} seconds.'

@Tool('scrape_tool',model=Scrape)
async def scrape_tool(url:str,**kwargs)->str:
    '''
    Extracts visible text content from the webpage currently displayed in the browser and returns it as markdown.

    This reads the rendered page content via the accessibility tree — not the raw HTML. Provide the URL of the page currently open in the browser. The output includes scroll position indicators so you know if there is more content above or below.

    Use when you need to read, analyze, or extract information from a webpage.
    '''
    desktop:_Desktop=kwargs['desktop']
    desktop_state=desktop.desktop_state
    tree_state=desktop_state.tree_state
    if not tree_state.dom_node:
        content=desktop.scrape(url)
        return f'URL:{url}\nContent:\n{content}'
    dom_node=tree_state.dom_node
    vertical_scroll_percent=dom_node.metadata.get('vertical_scroll_percent',0)
    content='\n'.join([node.text for node in tree_state.dom_informative_nodes])
    header_status = "[Reached top]" if vertical_scroll_percent <= 0 else f"[Scroll up ({vertical_scroll_percent*100:.2f}%) to see more content]"
    footer_status = "[Reached bottom]" if vertical_scroll_percent >= 100 else f"[Scroll down ({(1-vertical_scroll_percent)*100:.2f}%) to see more content]"
    return f'URL:{url}\nContent:\n{header_status}\n{content}\n{footer_status}'

@Tool('desktop_tool', model=Desktop)
async def desktop_tool(action: Literal['create', 'remove', 'rename', 'switch'], desktop_name: Optional[str] = None, new_name: Optional[str] = None, **kwargs) -> str:
    '''
    Manages Windows virtual desktops for workspace organization.

    - create: Creates a new virtual desktop. Optionally provide a name via desktop_name.
    - remove: Deletes the desktop specified by desktop_name. Ensure no needed windows remain on it.
    - rename: Renames desktop_name to new_name.
    - switch: Activates the desktop specified by desktop_name. Verify success in the next Desktop State.
    '''
    try:        
        match action:
            case 'create':
                # create_desktop(name) returns the name
                created_name = vdm_create(desktop_name)
                return f"Created desktop: '{created_name}'"
            case 'remove':
                if not desktop_name:
                    return "Error: desktop_name is required for removal."
                vdm_remove(desktop_name)
                return f"Removed desktop '{desktop_name}'"
            case 'rename':
                if not desktop_name or not new_name:
                    return "Error: desktop_name and new_name are required for rename."
                vdm_rename(desktop_name, new_name)
                return f"Renamed desktop '{desktop_name}' to '{new_name}'"
            case 'switch':
                if not desktop_name:
                    return "Error: desktop_name is required for switching."
                vdm_switch(desktop_name)
                return f"Switched to desktop '{desktop_name}'"
            case _:
                return f"Error: Unknown action: {action}"
    except Exception as e:
        return f"Error executing desktop action '{action}': {str(e)}"
