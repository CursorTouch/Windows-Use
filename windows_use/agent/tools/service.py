from windows_use.agent.tools.views import Click, Type, Scroll, Move, Shortcut, Wait, Scrape, Done, Shell, Memory, App, MultiSelect, MultiEdit, Desktop
from windows_use.vdm.core import create_desktop as vdm_create, remove_desktop as vdm_remove, rename_desktop as vdm_rename, switch_desktop as vdm_switch
from windows_use.agent.desktop.service import Desktop as _Desktop
from typing import Literal,Optional
from windows_use.tool import Tool
from pathlib import Path
from time import sleep

memory_path=Path.cwd()/'.memories'

@Tool('Done Tool',args_schema=Done)
def done_tool(answer:str,**kwargs):
    '''
    Signals task completion and provides the final answer to the user.
    
    Use this tool when you have successfully completed the requested task and have 
    a comprehensive answer ready. The answer should be well-formatted in markdown 
    and include all relevant information the user requested.
    '''
    return answer

@Tool('App Tool',args_schema=App)
def app_tool(mode:Literal['launch','resize','switch'],name:Optional[str]=None,loc:Optional[tuple[int,int]]=None,size:Optional[tuple[int,int]]=None,**kwargs)->str:
    '''
    Manages Windows applications through launch, resize, and window switching operations.
    
    Modes:
        - launch: Opens an application from the Windows Start Menu by name
        - resize: Adjusts the active application window's size and position
        - switch: Brings a specific application window into focus
    
    Use this tool to control application lifecycle and window management during task execution.
    '''
    desktop:_Desktop=kwargs['desktop']
    return desktop.app(mode,name,loc,size)

@Tool('Memory Tool',args_schema=Memory)
def memory_tool(mode: Literal['view','read','write','delete','update'],path: Optional[str] = None,
    content: Optional[str] = None,operation: Optional[Literal['replace', 'insert']] = 'replace',
    old_str: Optional[str] = None,new_str: Optional[str] = None,line_number: Optional[int] = None,
    read_range: Optional[tuple[int, int]] = None,**kwargs) -> str:
    '''
    Persistent file-based storage system for managing information across different task stages.
    
    Use this tool to:
        - Store important findings and data as md files in the .memories directory
        - Maintain context across complex multi-step operations
        - Track progress of plans and accumulate knowledge during task execution
        - Cache information that may be referenced in future steps
    
    Modes:
        - write: Create a new memory file (returns assigned path)
        - view: List all directories and memory files in the .memories directory
        - read: Retrieve contents of a specific memory file by path
            * read_range: Optional (start, end) tuple to read specific line range (0-indexed, end exclusive)
        - update: Modify contents of an existing memory file by path
            Operations:
            * replace: Replace old_str with new_str (requires old_str and new_str)
            * insert: Insert content at line_number (requires line_number and content)
        - delete: Remove a memory file by path
    
    All data is persisted as files in the .memories directory, ensuring information
    survives across sessions and can be shared between different task stages.
    
    Essential for tasks requiring information persistence and cross-stage data sharing.
    '''
    match mode:
        case 'view':
            files = (Path(path) if path else memory_path).rglob('*.md')
            result = '\n'.join([f'{i+1}. {file.relative_to(memory_path.parent).as_posix()}' 
                               for i, file in enumerate(files)])
            return result if result else "No memory files found."
        
        case 'write':
            file_path = memory_path / path if not Path(path).is_absolute() else Path(path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding='utf-8')
            return f'{file_path.name} created in {file_path.parent.relative_to(memory_path.parent).as_posix()}.'
        
        case 'read':
            file_path = memory_path / path if not Path(path).is_absolute() else Path(path)
            if not file_path.exists():
                return f'Error: {file_path.name} not found.'
            
            file_content = file_path.read_text(encoding='utf-8')
            
            if read_range:
                start, end = read_range
                lines = file_content.splitlines()
                
                if start < 0 or start >= len(lines):
                    return f'Error: start line {start} out of range (0-{len(lines)-1}).'
                if end < start or end > len(lines):
                    return f'Error: end line {end} out of range ({start}-{len(lines)}).'
                
                selected_lines = lines[start:end]
                return f"File: {file_path.relative_to(memory_path.parent).as_posix()}\nLines {start}-{end-1}:\n" + '\n'.join(selected_lines)
            
            return f"File: {file_path.relative_to(memory_path.parent).as_posix()}\nContent:\n{file_content}"
        
        case 'update':
            file_path = memory_path / path if not Path(path).is_absolute() else Path(path)
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
                    return f'{file_path.name} updated: replaced "{old_str[:50]}..." with "{new_str[:50]}...".'
                
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
            file_path = memory_path / path if not Path(path).is_absolute() else Path(path)
            if not file_path.exists():
                return f'Error: {file_path.name} not found.'
            
            file_path.unlink()
            return f'{file_path.name} deleted from {file_path.parent.relative_to(memory_path.parent).as_posix()}.'
        
    return "Invalid mode. Use 'view', 'write', 'read', 'update', or 'delete'."

@Tool('Shell Tool',args_schema=Shell)
def shell_tool(command: str,**kwargs) -> str:
    '''
    Executes PowerShell commands and returns output with status codes.
    
    Use this tool to:
        - Run Windows system commands and scripts
        - Query system information and configurations
        - Automate file operations and system tasks
        - Access Windows management utilities
    
    The working directory is set to the user's HOME directory by default. 
    Returns both command output and exit status code for error handling.
    '''
    desktop:_Desktop=kwargs['desktop']
    response,status=desktop.execute_command(command)
    return f'Response: {response}\nStatus Code: {status}'

@Tool('Click Tool',args_schema=Click)
def click_tool(loc:Optional[tuple[int,int]]=None,button:Literal['left','right','middle']='left',clicks:int=1,**kwargs)->str:
    '''
    Performs mouse click operations on UI elements at specified coordinates.
    
    Click patterns:
        - Single left click: Select elements, focus input fields
        - Double left click: Open apps, folders, files
        - Single right click: Open context menus
        - Middle click: Browser-specific actions
    
    Automatically detects UI elements under cursor and adjusts click behavior 
    for reliable interaction. Essential for all point-and-click UI operations.
    '''
    x,y=loc
    desktop:_Desktop=kwargs['desktop']
    desktop.click(loc,button,clicks)
    num_clicks={1:'Single',2:'Double',3:'Triple'}
    return f'{num_clicks.get(clicks)} {button} clicked at ({x},{y}).'

@Tool('Type Tool',args_schema=Type)
def type_tool(loc:Optional[tuple[int,int]]=None,text:str='',clear:Literal['true','false']='false',caret_position:Literal['start','idle','end']='idle',press_enter:Literal['true','false']='false',**kwargs):
    '''
    Types text into input fields, text areas, and focused UI elements.
    
    Features:
        - Click target element and input text automatically
        - Clear existing content before typing (clear='true')
        - Position caret at start, end, or leave idle
        - Optionally press Enter after typing
    
    Use for form filling, search queries, text editing, and any text input operation.
    The tool automatically clicks the target element coordinates to ensure focus before typing.
    '''
    x,y=loc
    desktop:_Desktop=kwargs['desktop']
    desktop.type(loc,text,clear,caret_position,press_enter)
    return f'Typed {text} at ({x},{y}).'

@Tool('Scroll Tool',args_schema=Scroll)
def scroll_tool(loc:Optional[tuple[int,int]]=None,type:Literal['horizontal','vertical']='vertical',direction:Literal['up','down','left','right']='down',wheel_times:int=1,**kwargs)->str:
    '''
    Scrolls content vertically or horizontally at specified or current cursor location.
    
    Use cases:
        - Navigate through long webpages and documents
        - Browse lists, tables, and scrollable containers
        - Access off-screen content in any scrollable area
    
    Parameters:
        - wheel_times: Controls scroll distance (1 wheel ≈ 3-5 lines of text)
        - direction: Scroll direction: 'up'/'down' for vertical, 'left'/'right' for horizontal
        - loc: Target coordinates (if None, scrolls at current cursor position)
    
    Essential tool for accessing content beyond the visible viewport.
    '''
    desktop:_Desktop=kwargs['desktop']
    response=desktop.scroll(loc,type,direction,wheel_times)
    if response:
        return response
    return f'Scrolled {type} {direction} by {wheel_times} wheel times.'

@Tool('Move Tool',args_schema=Move)
def move_tool(loc:tuple[int,int],drag:bool=False,**kwargs)->str:
    '''
    Moves mouse cursor to specific coordinates, optionally performing a drag operation.
    
    Use cases:
        - Hover over elements to reveal tooltips (drag=False)
        - Reposition cursor without clicking (drag=False)
        - Drag and drop items from current position (drag=True)
        - Move files/windows by dragging (drag=True)
    
    If drag is True, simulates holding the mouse button from start to end.
    '''
    x,y=loc
    desktop:_Desktop=kwargs['desktop']
    if drag:
        desktop.drag(loc)
        return f'Dragged the selected element to ({x},{y}).'
    else:
        desktop.move(loc)
        return f'Moved the mouse pointer to ({x},{y}).'

@Tool('Shortcut Tool',args_schema=Shortcut)
def shortcut_tool(shortcut:str,**kwargs)->str:
    '''
    Executes keyboard shortcuts for rapid command execution and navigation.
    
    Supports:
        - Single keys: 'enter', 'escape', 'tab', 'delete'
        - Key combinations: 'ctrl+c', 'alt+tab', 'ctrl+shift+n'
        - Multiple keys separated by '+' for simultaneous press
    
    Use for common operations like copy/paste, window switching, menu access, 
    and application-specific shortcuts. More efficient than mouse-based navigation 
    for many operations.
    '''
    desktop:_Desktop=kwargs['desktop']
    desktop.shortcut(shortcut)
    return f'Pressed {shortcut}.'

@Tool('Multi Select Tool',args_schema=MultiSelect)
def multi_select_tool(press_ctrl:Literal['true','false']='true',elements:list[tuple[int,int]]=[],**kwargs)->str:
    '''
    Selects mutiple items such as files, folders, or checkboxes if press_ctrl is true and perform redundant clicks if press_ctrl is false.

    Use cases:
        - Select multiple items in files, folders, or checkboxes
        - Mark multiple checkboxes in a form
        - Repeat clicks on same element
    
    Use for common operations like selecting multiple items or repeated clicks.
    '''
    desktop:_Desktop=kwargs['desktop']
    desktop.multi_select(press_ctrl,elements)
    return f'Multi-selected elements at {'\n'.join([f'({x},{y})' for x,y in elements])}.'

@Tool('Multi Edit Tool',args_schema=MultiEdit)
def multi_edit_tool(elements:list[tuple[int,int,str]],**kwargs)->str:
    '''
    Typing text into multiple input fields.
    
    Use cases:
        - Enter text into multiple text boxes
        - Fill in forms with multiple fields
        - Edit multiple lines of text
    
    Typing text into multiple input fields, text areas.
    '''
    desktop:_Desktop=kwargs['desktop']
    desktop.multi_edit(elements)
    return f'Multi-edited elements at {','.join([f'({x},{y}) text={text}' for x,y,text in elements])}.'

@Tool('Wait Tool',args_schema=Wait)
def wait_tool(duration:int,**kwargs)->str:
    '''
    Pauses execution for a specified duration to allow processes to complete.
    
    Essential for:
        - Waiting for applications to launch and initialize
        - Allowing webpages and content to fully load
        - Giving animations and transitions time to complete
        - Ensuring system operations finish before proceeding
    
    Use strategic waits to improve reliability when operations need time to complete.
    Duration is specified in seconds.
    '''
    sleep(duration)
    return f'Waited for {duration} seconds.'

@Tool('Scrape Tool',args_schema=Scrape)
def scrape_tool(url:str,**kwargs)->str:
    '''
    Fetches webpage content and converts it to clean markdown format for analysis.
    
    Use cases:
        - Extract text content from webpages for processing
        - Gather information from online sources
        - Convert HTML pages to structured, readable text
        - Access web data without browser automation
    
    Requires full URL including protocol (http:// or https://).
    NOTE: This tool reads the visual accessibility tree (what is currently rendered on screen),
    not the raw HTML source code. It captures visible text content accurately.
    Returns structured text suitable for parsing, analysis, and information extraction.
    '''
    desktop:_Desktop=kwargs['desktop']
    desktop_state=desktop.desktop_state
    tree_state=desktop_state.tree_state
    if not tree_state.dom_node:
        return f'Unable to scrape URL: {url}. No DOM node found.'
    dom_node=tree_state.dom_node
    vertical_scroll_percent=dom_node.vertical_scroll_percent
    content='\n'.join([node.text for node in tree_state.dom_informative_nodes])
    header_status = "Reached top" if vertical_scroll_percent <= 0 else "Scroll up to see more"
    footer_status = "Reached bottom" if vertical_scroll_percent >= 100 else "Scroll down to see more"
    return f'URL:{url}\nContent:\n{header_status}\n{content}\n{footer_status}'

@Tool('Desktop Tool', args_schema=Desktop)
def desktop_tool(action: Literal['create', 'remove', 'rename', 'switch', 'get_all'], desktop_id: Optional[str] = None, name: Optional[str] = None, **kwargs) -> str:
    '''
    Manages Windows virtual desktops.
    
    Actions:
        - create: Create a new virtual desktop (optional: provide name)
        - remove: Remove a virtual desktop by ID
        - rename: Rename a virtual desktop by ID
        - switch: Switch to a virtual desktop by ID
        - get_all: List all virtual desktops with their IDs and names
        
    Use this tool to organize workspaces and manage virtual desktops programmatically.
    '''
    try:
        match action:
            case 'create':
                new_id = vdm_create(name)
                return f"Created desktop with ID: {new_id}" + (f" and name '{name}'" if name else "")
            case 'remove':
                if not desktop_id:
                    return "Error: desktop_id is required for removal."
                vdm_remove(desktop_id)
                return f"Removed desktop {desktop_id}"
            case 'rename':
                if not desktop_id or not name:
                    return "Error: desktop_id and name are required for rename."
                vdm_rename(desktop_id, name)
                return f"Renamed desktop {desktop_id} to '{name}'"
            case 'switch':
                if not desktop_id:
                    return "Error: desktop_id is required for switching."
                vdm_switch(desktop_id)
                return f"Switched to desktop {desktop_id}"
            case _:
                return f"Unknown action: {action}"
    except Exception as e:
        return f"Error executing desktop action '{action}': {str(e)}"