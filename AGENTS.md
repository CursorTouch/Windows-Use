# Windows Use

## Description

Windows Use is an AI Agent that interacts with Windows OS at GUI level. Basically computer use for windows operating system. The project operates on the top of the Windows UI Automation API (UIA3) and Virtual Desktop Manager (VDM) API.

## How it works

Windows Use uses a combination of tools to interact with the Windows OS. It uses the accessibility tree to get the UI elements and then uses the tools to interact with the UI elements.

## Tools

Windows Use has the following tools:

- **App Tool**: Manages Windows applications (launch, resize, switch).
- **Click Tool**: Performs mouse clicks (left, right, middle, single, double) at specific coordinates.
- **Drag Tool**: Performs drag-and-drop operations from the current cursor location to a destination.
- **Done Tool**: Signals the successful completion of a task and returns the final answer.
- **Memory Tool**: Provides persistent file-based storage (`.windows-use/memories` dir in user home) to read, write, update, delete, and view memory files. Useful for saving context and sharing data.
- **File Tool**: Performs file system operations: read, write, list, delete, move, copy, or check existence. Use for config files, outputs, and file organization.
- **Move Tool**: Moves the mouse cursor to specific coordinates without clicking (hovering).
- **Multi Edit Tool**: Types text into multiple input fields in a batch operation.
- **Multi Select Tool**: Selects multiple items (files, folders, checkboxes) or performs repetitive clicks.
- **Scrape Tool**: Fetches webpage content and converts it to markdown. Note: Reads from the visual accessibility tree.
- **Scroll Tool**: Scrolls content vertically or horizontally.
- **Shell Tool**: Executes PowerShell commands and returns output with status codes.
- **Shortcut Tool**: Executes keyboard shortcuts (e.g., `ctrl+c`, `alt+tab`).
- **Type Tool**: Types text into focused UI elements, with options to clear text or press Enter.
- **Wait Tool**: Pauses execution for a specified duration to allow processes or UI animations to complete.

## Agent Config:
- `mode`: the agent has two modes, `flash` and `normal`.
    - `flash`: The agent will use the flash prompt to generate the response. (Lightweight)
    - `normal`: The agent will use the normal prompt to generate the response.
- `max_steps`: Maximum number of steps the agent can take to complete the task.
- `llm`: LLM to be used by the agent.
- `browser`: Browser to be used by the agent.
- `use_vision`: Screenshot will be given to the LLM if true.
- `use_annotation`: Annotated screenshot will be given to the LLM if true.
- `auto_minimize`: Minimize the window of the agent running interface (temporarily).

## Key Commands
The project uses `uv` as the package manager.
- `uv sync` to install dependencies and create virtual environment.
- `uv run main.py` to start the agent.
- `uv add windows-use` to add the package to the existing project.

## Testing

- `pytest` to run all tests.

## Project Structure

- `windows_use/llms` - To access different LLMs.
- `windows_use/agent` - Core Agent implementation (includes tools, prompts, etc.)
- `windows_use/agent/tools` - Tools used by the agent to interact with the Windows OS.
- `windows_use/agent/prompt` - Managing the prompts of the agent (includes the system_prompt, observation,..etc).
- `windows_use/agent/desktop` - Desktop Module containing high level information about the windows OS (Windows, Desktop, Taskbar, Start Menu, etc.)
- `windows_use/agent/tree` - Tree Module containing information about the UI elements in the Windows or Apps.
- `windows_use/agent/registry` - Registry contains the tools owned by the agent.
- `windows_use/agent/watchdog` - Watchdog used for monitoring the Operating system events.
- `windows_use/uia` - UIA (UI Automation) Module the way to access the Windows UIA3 API
- `windows_use/vdm` - VDM (Virtual Desktop Manager) Module the way to access the Windows VDM API
- `windows_use/tool` - The Tool Module used to implement the tools for the agent.
- `windows_use/messages` - Messages Module used to implement varrious kinds of message formats for the LLM (includes SystemMessage,HumanMessage,AIMessage,..etc)
- `windows_use/telemetry` - Telemetry Module used to track the usage of the agent.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Security

- This project has the ability to operate ones windows OS at GUI level. So be careful while using this project.
- Best pratice launch the project in a virtual machine, so that if something goes wrong, you can revert the changes.