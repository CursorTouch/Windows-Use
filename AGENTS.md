# Agents

This project defines a single, versatile agent named **Windows Use**. This agent is designed to interact with the Windows Operating System through its Graphical User Interface (GUI), file system, and shell, effectively mimicking a human user.

## Windows Use

The **Windows Use** agent acts as an autonomous operator capable of performing a wide range of tasks on a Windows machine. It leverages a suite of specialized tools to perceive the desktop state and execute actions.

### Capabilities

*   **GUI Interaction:** Can click, type, scroll, drag, move the mouse, and use keyboard shortcuts.
*   **Application Management:** Can launch, switch, and resize application windows.
*   **System Control:** Can execute PowerShell commands to interact with the OS at a lower level.
*   **Memory Management:** Maintains a persistent memory store to save findings, plans, and context across steps.
*   **Web Interaction:** Can scrape content from webpages (via accessibility tree retrieval).

### Configuration

The agent is highly configurable and can be instantiated with different parameters:

*   **LLM (Large Language Model):** Compatible with various providers including Google (Gemini), Anthropic (Claude), Mistral, and Ollama (local models).
*   **Browser:** Configurable default browser (default: Edge).
*   **Vision:** Option to enable vision capabilities (`use_vision=True`) to allow the agent to "see" the desktop screenshot.
*   **Auto Minimize:** Option to minimize the console window when the agent runs (`auto_minimize=True`).
*   **Telemetry:** You can disable anonymized telemetry by setting the environment variable `ANONYMIZED_TELEMETRY` to `False`.

### Tools

The agent has access to the following registry of tools:

| Tool Name | Description |
| :--- | :--- |
| **App Tool** | Manages Windows applications (launch, resize, switch). |
| **Click Tool** | Performs mouse clicks (left, right, middle, single, double) at specific coordinates. |
| **Drag Tool** | Performs drag-and-drop operations from the current cursor location to a destination. |
| **Done Tool** | Signals the successful completion of a task and returns the final answer. |
| **Memory Tool** | Provides persistent file-based storage (`.memories` dir) to read, write, update, delete, and view memory files. Useful for saving context and sharing data. |
| **Move Tool** | Moves the mouse cursor to specific coordinates without clicking (hovering). |
| **Multi Edit Tool** | Types text into multiple input fields in a batch operation. |
| **Multi Select Tool** | Selects multiple items (files, folders, checkboxes) or performs repetitive clicks. |
| **Scrape Tool** | Fetches webpage content and converts it to markdown. Note: Reads from the visual accessibility tree. |
| **Scroll Tool** | Scrolls content vertically or horizontally. |
| **Shell Tool** | Executes PowerShell commands and returns output with status codes. |
| **Shortcut Tool** | Executes keyboard shortcuts (e.g., `ctrl+c`, `alt+tab`). |
| **Type Tool** | Types text into focused UI elements, with options to clear text or press Enter. |
| **Wait Tool** | Pauses execution for a specified duration to allow processes or UI animations to complete. |

## Usage

The agent is typically initialized in `main.py` and runs an interactive loop where it accepts user queries and executes actions until the task is done or valid steps are exhausted.

```python
# Example Initialization
agent = Agent(
    llm=llm_instance,
    browser=Browser.EDGE,
    use_vision=False
)
agent.print_response(query="Open Notepad and write 'Hello World'")
```

## Modules

The project is structured into several key modules that work together to power the agent:

### 1. Agent Module (`windows_use.agent`)
The core orchestrator of the system.
*   **`desktop`**: Handles low-level interactions with the Windows desktop.
    *   **Operation:** It uses `uiautomation` to inspect the UI tree and `pyautogui` for input simulation (clicking, typing, scrolling).
    *   **App Management:** It identifies running applications, manages their window states (minimize, maximize, restore), and handles resizing.
    *   **Execution:** It executes PowerShell commands for system-level operations like launching apps or querying system info.
*   **`tree`**: Responsible for converting the raw Windows Accessibility Tree into a structured, agent-friendly format.
    *   **Filtering:** It actively filters out non-essential elements (off-screen, invisible, or non-interactive items) to reduce noise for the LLM.
    *   **Parallel Processing:** Uses `ThreadPoolExecutor` to fetch UI nodes from multiple applications concurrently, ensuring performance.
    *   **DOM Handling:** It has special logic to detect web content (`RootWebArea`) and treat it as a "DOM" structure, extracting headers, links, and inputs more effectively.
    *   **Vision Support:** Generates annotated screenshots where interactive elements are highlighted with bounding boxes and numeric labels, allowing the vision-enabled agent to "see" and click targets.
*   **`registry`**: Manages the registration and execution of tools. It acts as the bridge between the high-level agent logic and the concrete tool implementations.
*   **`prompt`**: Dynamic prompt generation engine that constructs system instructions and observation prompts based on the current desktop state and task history.
*   **`tools`**: Contains the concrete implementations of all available tools (`click_tool`, `type_tool`, `shell_tool`, etc.).

### 2. LLMs Module (`windows_use.llms`)
Provides a unified interface for interacting with various Large Language Models.
*   **Supported Providers:** Google (Gemini), Anthropic (Claude), OpenAI, Mistral, Ollama (local models), Groq, Cerebras, and OpenRouter.
*   **Abstraction:** Abstracts away the differences between APIs, allowing the agent to switch models easily via configuration.

### 3. Messages Module (`windows_use.messages`)
Defines the standard message format used for communication between the agent and the LLMs.
*   **Types:** Includes `SystemMessage`, `HumanMessage`, `AIMessage`, and `ImageMessage` (for handling screenshots).

### 4. Telemetry Module (`windows_use.telemetry`)
Handles logging and analytics.
*   **Functions:** Captures agent steps, errors, success rates, and token usage for debugging and performance monitoring.

### 5. Tool Module (`windows_use.tool`)
Provides the foundational infrastructure for creating tools.
*   **Base:** Defines the base classes and decorators used to creating new tools that are compatible with the agent's registry.

## Security

**⚠️ Critical Notice:** The **Windows Use** agent directly interacts with your operating system's GUI and shell with the **same privileges as the user running the process**. It does **NOT** run in a sandbox by default.

### Risks
Because the agent can execute shell commands, manage files, and control the mouse/keyboard, it has the potential to:
*   Delete or modify important files.
*   Change system settings.
*   Install or uninstall software.
*   Access sensitive information visible on screen or in files.

### Recommendations
To ensure safety, it is **STRONGLY RECOMMENDED** to follow these practices:
1.  **Use a Virtual Machine:** Run the agent inside a VM (VirtualBox, VMware, Hyper-V) or Windows Sandbox to isolate it from your main system.
2.  **Dedicated User:** If running on a host machine, consider using a dedicated standard user account with limited privileges.
3.  **Monitor Execution:** Always watch the agent's actions in real-time and be ready to terminate the process (`Ctrl+C`) if it attempts unsafe operations.

For a detailed security policy and comprehensive best practices, please refer to [SECURITY.md](SECURITY.md).

