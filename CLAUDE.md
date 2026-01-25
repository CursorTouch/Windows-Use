# CLAUDE.md - AI Assistant Guide for Windows-Use

> **Last Updated**: 2026-01-25
> **Version**: 0.7.0
> **For**: AI Assistants working on the Windows-Use codebase

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Repository Structure](#repository-structure)
3. [Architecture & Design Patterns](#architecture--design-patterns)
4. [Development Workflow](#development-workflow)
5. [Code Conventions](#code-conventions)
6. [Testing Guidelines](#testing-guidelines)
7. [Key Modules Deep Dive](#key-modules-deep-dive)
8. [Working with Tools](#working-with-tools)
9. [LLM Provider Integration](#llm-provider-integration)
10. [Event System](#event-system)
11. [Security Considerations](#security-considerations)
12. [Common Tasks & Patterns](#common-tasks--patterns)
13. [Troubleshooting](#troubleshooting)

---

## Project Overview

**Windows-Use** is a sophisticated AI automation agent that enables Large Language Models (LLMs) to interact directly with Windows OS at the GUI layer without relying on traditional computer vision models.

### Key Facts
- **Language**: Python 3.13+
- **Platform**: Windows 7-11 only (Windows API dependency)
- **License**: MIT
- **Build System**: Hatchling
- **Package Manager**: UV (preferred) or pip
- **Repository**: https://github.com/CursorTouch/Windows-Use

### Core Capabilities
- **GUI Automation**: Mouse clicks, keyboard input, drag-and-drop, shortcuts
- **Application Management**: Launch, switch, resize, minimize/maximize windows
- **Shell Execution**: PowerShell command execution with output capture
- **UI State Extraction**: Windows UI Automation (UIA) tree parsing
- **Vision Support**: Optional screenshot annotation for vision-enabled LLMs
- **Event Monitoring**: Real-time UI state change detection via COM interfaces
- **Memory System**: Persistent file-based storage for agent context

---

## Repository Structure

```
/home/user/Windows-Use/
├── windows_use/                    # Main source package
│   ├── agent/                      # Core agent orchestration
│   │   ├── service.py              # Agent class - main entry point
│   │   ├── views.py                # Data models (AgentStep, AgentResult, AgentData)
│   │   ├── utils.py                # Agent utilities (extract_agent_data from LLM output)
│   │   ├── desktop/                # Desktop abstraction layer
│   │   │   ├── service.py          # Desktop state management & app control
│   │   │   ├── views.py            # Desktop data models (App, DesktopState, Size)
│   │   │   └── config.py           # Browser names, excluded/avoided apps, DPI config
│   │   ├── tree/                   # UI element tree parsing
│   │   │   ├── service.py          # Tree service - builds UI element hierarchy
│   │   │   ├── views.py            # Tree data models (TreeElementNode, TreeState, BoundingBox)
│   │   │   ├── config.py           # Control type classifications
│   │   │   └── utils.py            # Bounding box utilities
│   │   ├── tools/                  # Tool implementations (14 tools)
│   │   │   ├── service.py          # Tool functions (click, type, shell, scroll, etc.)
│   │   │   └── views.py            # Tool input schemas (Pydantic models)
│   │   ├── registry/               # Tool registry & execution
│   │   │   ├── service.py          # Tool registry & execution orchestrator
│   │   │   └── views.py            # ToolResult model
│   │   ├── prompt/                 # Prompt templates & construction
│   │   │   ├── service.py          # Prompt builder service
│   │   │   ├── system.md           # System prompt template
│   │   │   ├── observation.md      # Current state template
│   │   │   ├── action.md           # Action output template
│   │   │   ├── answer.md           # Final answer template
│   │   │   └── previous_observation.md  # Step context template
│   │   └── watchdog/               # Event monitoring & callbacks
│   │       └── service.py          # WatchDog - UIAutomation event handlers
│   ├── llms/                       # LLM provider integrations (8 providers)
│   │   ├── base.py                 # BaseChatLLM protocol
│   │   ├── anthropic.py            # Anthropic (Claude) integration
│   │   ├── google.py               # Google Gemini integration
│   │   ├── openai.py               # OpenAI integration
│   │   ├── ollama.py               # Ollama local model integration
│   │   ├── groq.py                 # Groq API integration
│   │   ├── mistral.py              # Mistral AI integration
│   │   ├── cerebras.py             # Cerebras integration
│   │   ├── open_router.py          # OpenRouter integration
│   │   └── views.py                # ChatLLMResponse, ChatLLMUsage models
│   ├── uia/                        # Windows UI Automation wrapper
│   │   ├── core.py                 # UIAutomation COM interface client
│   │   ├── enums.py                # Control types, patterns, events (50+ types)
│   │   ├── controls.py             # Control classes
│   │   ├── patterns.py             # UIAutomation patterns
│   │   └── events.py               # Event IDs (36+ event types)
│   ├── messages/                   # Message types for LLM conversation
│   │   └── service.py              # SystemMessage, HumanMessage, AIMessage, ImageMessage
│   ├── tool/                       # Tool decorator & execution framework
│   │   └── service.py              # Tool class decorator
│   ├── vdm/                        # Virtual Desktop Manager
│   │   └── core.py                 # Windows 10/11 VDM API wrapper
│   └── telemetry/                  # Analytics & telemetry (PostHog)
│       ├── service.py              # ProductTelemetry
│       └── views.py                # Telemetry event models
├── tests/                          # Test suite (pytest)
│   ├── unit/                       # Unit tests
│   │   ├── agent/                  # Agent tests
│   │   ├── desktop/                # Desktop tests
│   │   └── tree/                   # Tree tests
│   └── test_uia_implementation.py  # UIA integration tests
├── main.py                         # Example usage entry point
├── pyproject.toml                  # Project configuration
├── uv.lock                         # UV dependency lock file
├── README.md                       # Project documentation
├── SECURITY.md                     # Security guidelines
├── CONTRIBUTING.md                 # Contribution guidelines
└── AGENTS.md                       # Agent documentation
```

### File Organization Pattern
- **service.py**: Contains business logic and service classes
- **views.py**: Contains Pydantic data models and schemas
- **config.py**: Contains configuration constants and mappings
- **utils.py**: Contains utility functions
- **__init__.py**: Package exports

---

## Architecture & Design Patterns

### Layered Architecture

```
┌─────────────────────────────────────┐
│  Agent (Orchestrator)               │  ← Main entry point, manages loop
├─────────────────────────────────────┤
│  Tool Registry + Tool Execution     │  ← Tool management & validation
├─────────────────────────────────────┤
│  Desktop Service (App Management)   │  ← Window management, shell execution
├─────────────────────────────────────┤
│  Tree Service (UI State Building)   │  ← UI element extraction & filtering
├─────────────────────────────────────┤
│  UIA Layer (Windows COM)            │  ← Windows UI Automation interface
└─────────────────────────────────────┘
```

### Design Patterns Used

#### 1. **Service Layer Pattern**
- Each module separates logic (service.py) from data models (views.py)
- Example: `agent/desktop/service.py` + `agent/desktop/views.py`

#### 2. **Decorator Pattern**
- `@Tool()` decorator for registering tool functions
- Automatically handles schema preprocessing and invocation

```python
@Tool(name="click_tool", description="...", args_schema=ClickInput)
def click_tool(x: int, y: int, button: str = "left", count: int = 1):
    # Implementation
```

#### 3. **Protocol/Interface Pattern**
- `BaseChatLLM` as Protocol for provider duck-typing
- Enables flexible LLM provider swapping

```python
class BaseChatLLM(Protocol):
    model_name: str
    provider: str
    def invoke(self, messages: list, structured_output: dict = None): ...
```

#### 4. **Registry Pattern**
- `Registry` class manages tool collection
- Dynamic tool execution by name with validation

#### 5. **Observer Pattern** (Event Handling)
- `WatchDog` with callback registration
- COM event handlers trigger callbacks on UI changes

#### 6. **Template Method Pattern**
- Prompt templates with variable substitution
- `Prompt` service builds complete prompts from markdown templates

#### 7. **Context Manager Pattern**
- `WatchDog` as context manager for event thread lifecycle
- `Desktop.auto_minimize()` for window management

```python
with self.watchdog:
    # Event monitoring active
    with self.desktop.auto_minimize():
        # Console minimized
```

### Concurrency Model

#### Threading Strategy
1. **Tree Extraction**: Uses `ThreadPoolExecutor` for parallel app processing
2. **Event Monitoring**: Dedicated STA (Single-Threaded Apartment) thread for COM events
3. **Retry Logic**: `THREAD_MAX_RETRIES = 3` for failed threads

#### Caching Strategy (Performance)
To minimize expensive cross-process COM calls, Windows-Use implements **UIA Caching**:
- **CacheRequest**: Batches property and pattern requests into a single COM call.
- **Tree Traversal Optimization**: The tree service uses `CacheRequestFactory` to pre-fetch common properties (Name, ControlType, BoundingBox) for all children of a node simultaneously.
- **Benefit**: Reduces the number of COM round-trips from $O(N \times P)$ to $O(N)$ where $P$ is the number of properties.

```python
# Tree service uses parallel processing and caching
with ThreadPoolExecutor(max_workers=max(len(other_apps), 1)) as executor:
    futures = {executor.submit(self.get_nodes, app, ...): app for app in other_apps}
```

---

## Development Workflow

### Setup & Installation

#### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/windows-use.git
cd windows-use
```

#### 2. Install Dependencies
```bash
# Using UV (preferred)
uv add windows-use

# Or using pip
pip install -e ".[dev]"
```

#### 3. Install Pre-commit Hooks
```bash
pip install pre-commit
pre-commit install
```

### Branching Strategy
- **main**: Latest stable code
- **feature/your-feature-name**: Feature branches
- **fix/bug-description**: Bug fix branches

### Commit Messages
- No strict style enforced
- Keep messages informational and clear
- Good: "Add event handler for structure changes"
- Avoid: "fix stuff", "update"

### Code Quality Tools

#### Ruff (Linter & Formatter)
```bash
ruff check windows_use/         # Check code style
ruff format windows_use/        # Auto-format code
```

**Configuration** (from pyproject.toml):
- Line length: 100 characters
- Use double quotes for strings
- Follow PEP 8 naming conventions

#### Pre-commit Hooks
The hooks automatically:
- Format code using Ruff
- Run linting checks
- Check for trailing whitespace
- Ensure files end with newline
- Validate YAML files
- Check for large files
- Remove debug statements

---

## Code Conventions

### Python Style Guidelines

#### Type Hints
**ALWAYS** use type hints for function signatures:

```python
# Good
def get_state(self, use_vision: bool = False) -> DesktopState:
    ...

# Bad
def get_state(self, use_vision=False):
    ...
```

#### Docstrings
Use Google-style docstrings:

```python
def function_name(param1: type, param2: type) -> return_type:
    """Short description.

    Longer description if needed.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ExceptionType: When and why this exception is raised
    """
```

#### Naming Conventions
- **Classes**: PascalCase (e.g., `AgentStep`, `DesktopState`)
- **Functions/Methods**: snake_case (e.g., `get_state`, `extract_agent_data`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `THREAD_MAX_RETRIES`, `BROWSER_NAMES`)
- **Private Methods**: Prefix with `_` (e.g., `_on_focus_change`)

#### Pydantic Models
All data models use Pydantic for validation:

```python
from pydantic import BaseModel, Field

class ClickInput(BaseModel):
    x: int = Field(..., description="X coordinate")
    y: int = Field(..., description="Y coordinate")
    button: str = Field("left", description="Mouse button")
    count: int = Field(1, description="Number of clicks")
```

### Module Organization

#### Standard Module Structure
```python
# 1. Standard library imports
import logging
from contextlib import nullcontext
from concurrent.futures import ThreadPoolExecutor

# 2. Third-party imports
from pydantic import BaseModel
from rich.console import Console

# 3. Local imports
from windows_use.agent.views import AgentResult
from windows_use.llms.base import BaseChatLLM

# 4. Logger setup (if needed)
logger = logging.getLogger(__name__)

# 5. Constants
MAX_RETRIES = 3

# 6. Class/function definitions
class MyClass:
    ...
```

### Error Handling

#### Use Specific Exceptions
```python
# Good
try:
    result = self.llm.invoke(messages)
except ValueError as e:
    logger.error(f"Invalid input: {e}")
except ConnectionError as e:
    logger.error(f"Network error: {e}")

# Avoid
try:
    result = self.llm.invoke(messages)
except Exception as e:
    logger.error(f"Error: {e}")
```

#### Retry Logic Pattern
```python
for attempt in range(1, max_retries + 1):
    try:
        result = operation()
        break
    except Exception as e:
        logger.error(f"Attempt {attempt}/{max_retries} failed: {e}")
        if attempt == max_retries:
            raise
```

### Logging Conventions

```python
logger.info(f"[Agent] 🎯 Step: {step}/{max_steps}")
logger.error(f"[LLM]: {error}. Retrying attempt {n}/{max}...")
logger.debug(f"[Desktop] Found {len(apps)} applications")
```

---

## Testing Guidelines

### Test Framework
- **Framework**: pytest
- **Mocking**: unittest.mock (MagicMock, patch)
- **Coverage**: Aim for high coverage on new code

### Running Tests

```bash
# Run all tests
pytest

# Run specific module
pytest tests/unit/agent/

# Verbose output
pytest -v

# Short traceback
pytest --tb=short

# Run with coverage
pytest --cov=windows_use
```

### Test Organization

```
tests/
├── unit/                           # Unit tests
│   ├── agent/                      # Agent module tests
│   ├── desktop/                    # Desktop module tests
│   └── tree/                       # Tree module tests
└── test_uia_implementation.py      # Integration tests
```

### Writing Tests

#### Unit Test Pattern
```python
import pytest
from unittest.mock import MagicMock, patch

def test_agent_invoke():
    """Test agent invocation with valid query."""
    # Arrange
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = "response"
    agent = Agent(llm=mock_llm)

    # Act
    result = agent.invoke("test query")

    # Assert
    assert result.is_done
    mock_llm.invoke.assert_called_once()
```

#### Parametrized Tests
```python
@pytest.mark.parametrize("control_type,expected", [
    ("Button", True),
    ("Text", False),
    ("Edit", True),
])
def test_is_interactive(control_type, expected):
    assert is_interactive_control(control_type) == expected
```

#### Mocking External Dependencies
```python
@patch('windows_use.agent.desktop.service.pyautogui')
def test_click_tool(mock_pyautogui):
    result = click_tool(x=100, y=200, button="left")
    mock_pyautogui.click.assert_called_with(100, 200, button="left")
```

### Test Markers
```python
@pytest.mark.slow          # For slow tests
@pytest.mark.integration   # For integration tests
@pytest.mark.skip(reason="Requires Windows")  # Skip on CI
```

---

## Key Modules Deep Dive

### 1. Agent Module (`windows_use/agent/service.py`)

**Responsibility**: Main orchestrator for the agent loop

#### Key Class: `Agent`

```python
class Agent:
    def __init__(
        self,
        instructions: list[str] = [],
        browser: Browser = Browser.EDGE,
        llm: BaseChatLLM = None,
        max_consecutive_failures: int = 3,
        max_steps: int = 25,
        use_vision: bool = False,
        auto_minimize: bool = False
    ):
        self.registry = Registry([...])  # 14 tools
        self.desktop = Desktop()
        self.watchdog = WatchDog()
        self.telemetry = ProductTelemetry()
        # ...
```

#### Key Methods

**`invoke(query: str) -> AgentResult`**
- Main entry point for agent execution
- Sets up event monitoring via watchdog
- Manages agent loop with step counting
- Handles LLM retry logic
- Returns final result with success/failure status

**Agent Loop Flow**:
1. Initialize desktop state
2. Build system and observation prompts
3. Enter loop (up to `max_steps`)
4. Call LLM with current state
5. Extract action from LLM response
6. Execute tool via registry
7. Update state and messages
8. Repeat until done or max steps reached

### 2. Desktop Module (`windows_use/agent/desktop/service.py`)

**Responsibility**: Desktop state management and app control

#### Key Methods

**`get_state(use_vision: bool) -> DesktopState`**
- Captures current desktop state
- Gets active and background apps
- Builds UI tree via Tree service
- Optionally generates annotated screenshot

**`app(name: str, status: str, width: int, height: int) -> str`**
- Launches, switches to, or resizes applications
- Handles window state changes (minimize/maximize/restore)

**Virtual Desktop Management (`vdm` module)**:
- Supports Windows 10 and 11 virtual desktops.
- Capabilities: Create, remove, rename, and switch desktops.
- Uses internal Windows internal COM interfaces (`IVirtualDesktopManagerInternal`).

**`execute_shell_command(command: str) -> tuple[str, int]`**
- Executes PowerShell commands
- Returns output and exit code

**`scrape_element_text(element_id: int) -> str`**
- Extracts text content from UI elements
- Converts to markdown for web content

### 3. Tree Module (`windows_use/agent/tree/service.py`)

**Responsibility**: UI element extraction and state building

#### Key Methods

**`get_state(active_app: App, other_apps: list[App]) -> TreeState`**
- Builds complete UI tree for all apps
- Parallel processing with ThreadPoolExecutor
- Returns interactive, scrollable, and informative elements

**Performance: UIA Caching (`cache_utils.py`)**
- `CacheRequestFactory`: Creates optimized `CacheRequest` objects.
- `CachedControlHelper`: Wraps controls with cached properties.
- Tree traversal uses `node.CachedProperty` instead of `node.Property` for 10x speedup.

**`get_nodes(handle: int, ...)`**
- Recursively extracts UI elements from control handle.
- Filters by visibility, interactivity, screen bounds.
- Categorizes into interactive/scrollable/informative.

**`is_element_visible(element: Control) -> bool`**
- Checks bounding box intersection with screen.
- Validates minimum visible area threshold.

**`annotated_screenshot()`** (via `desktop`)
- Generates screenshot with element IDs overlaid.
- For vision-enabled LLMs.

#### Element Classification

**Interactive Elements** (Clickable/Editable):
- Button, Edit, ComboBox, CheckBox, RadioButton, Hyperlink, etc.
- Format: `id|app|type|name|val|keys|coords|focus`

**Scrollable Elements**:
- Pane, Document, List with scroll patterns
- Format: `id|app|type|name|coords|h_scroll|h_pct|v_scroll|v_pct|focus`

**Informative Elements** (Non-interactive):
- Text, Image, StatusBar, Separator
- Not sent to LLM (filtered out)

### 4. Tool System (`windows_use/agent/tools/service.py`)

#### Available Tools (15 total)

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `done_tool` | Signals task completion | `answer: str` |
| `app_tool` | Launch/resize/switch apps | `name, status, width, height` |
| `desktop_tool`| Create/switch/rename virtual desktops | `action, desktop_name, new_name` |
| `memory_tool` | File-based persistent storage | `action, key, value` |
| `click_tool` | Mouse clicks | `x, y, button, count` |
| `type_tool` | Text input | `text, id, clear, enter` |
| `scroll_tool` | Scrolling | `direction, id` |
| `move_tool` | Mouse movement & Drag | `to_x, to_y, button` |
| `shortcut_tool`| Keyboard shortcuts | `keys` |
| `shell_tool` | Execute commands | `command` |
| `scrape_tool` | Extract webpage text | `id` |
| `multi_select_tool`| Multi-select items | `ids` |
| `multi_edit_tool`| Multi-line editing | `entries` |
| `wait_tool` | Delay | `duration` |

#### Creating New Tools

```python
from windows_use.tool import Tool
from pydantic import BaseModel, Field

class MyToolInput(BaseModel):
    param1: str = Field(..., description="Description")
    param2: int = Field(default=0, description="Description")

@Tool(
    name="my_tool",
    description="What this tool does",
    args_schema=MyToolInput
)
def my_tool(param1: str, param2: int = 0) -> str:
    """Implementation."""
    # Do work
    return "Success"
```

Then register in `Agent.__init__`:
```python
self.registry = Registry([
    # ... existing tools
    my_tool
])
```

### 5. Registry Module (`windows_use/agent/registry/service.py`)

**Responsibility**: Tool management and execution

#### Key Methods

**`execute(tool_name: str, **kwargs) -> ToolResult`**
- Validates tool exists
- Validates input parameters via Pydantic
- Executes tool function
- Returns ToolResult with success/failure status

**`get_tools_prompt() -> str`**
- Generates tool documentation for LLM
- Includes tool names, descriptions, and schemas

---

## Working with Tools

### Tool Execution Flow

```
LLM Response → extract_agent_data() → Registry.execute() → Tool Function → ToolResult
```

### Tool Input Validation

All tool inputs are validated using Pydantic schemas:

```python
class ClickInput(BaseModel):
    x: int = Field(..., description="X coordinate to click", ge=0)
    y: int = Field(..., description="Y coordinate to click", ge=0)
    button: str = Field("left", description="Mouse button",
                       pattern="^(left|right|middle)$")
    count: int = Field(1, description="Number of clicks", ge=1, le=3)
```

**Benefits**:
- Automatic validation before execution
- Clear error messages for invalid inputs
- JSON schema generation for LLM documentation
- Type safety

### Memory Tool Usage

The memory tool provides persistent storage in `.memories` directory:

```python
# Write/Update memory
memory_tool(action="write", key="user_preferences", value="dark_mode")

# Read memory
result = memory_tool(action="read", key="user_preferences")

# Delete memory
memory_tool(action="delete", key="user_preferences")

# List all memories
result = memory_tool(action="list")
```

**Storage Location**: `.memories/` directory (gitignored)

---

## LLM Provider Integration

### Provider Architecture

All providers implement the `BaseChatLLM` protocol:

```python
class BaseChatLLM(Protocol):
    model_name: str
    provider: str

    def invoke(
        self,
        messages: list,
        structured_output: dict = None
    ) -> str:
        ...
```

### Supported Providers (8 total)

1. **Anthropic** (`anthropic.py`) - Claude models with thinking budget
2. **Google** (`google.py`) - Gemini with extended thinking
3. **OpenAI** (`openai.py`) - GPT models
4. **Ollama** (`ollama.py`) - Local models
5. **Groq** (`groq.py`) - Fast inference API
6. **Mistral** (`mistral.py`) - Mistral models
7. **Cerebras** (`cerebras.py`) - GPU acceleration
8. **OpenRouter** (`open_router.py`) - Multi-model router

### Adding a New Provider

1. Create `windows_use/llms/your_provider.py`:

```python
from windows_use.llms.base import BaseChatLLM
from windows_use.llms.views import ChatLLMResponse, ChatLLMUsage

class ChatYourProvider:
    def __init__(self, model: str, api_key: str, **kwargs):
        self.model_name = model
        self.provider = "your_provider"
        self.client = YourProviderClient(api_key=api_key)

    def serialize_messages(self, messages: list) -> list:
        """Convert internal messages to provider format."""
        return [{"role": msg.role, "content": msg.content} for msg in messages]

    def invoke(self, messages: list, structured_output: dict = None) -> str:
        """Call provider API."""
        serialized = self.serialize_messages(messages)
        response = self.client.chat(messages=serialized, model=self.model_name)
        return response.content
```

2. Export in `windows_use/llms/__init__.py`:

```python
from windows_use.llms.your_provider import ChatYourProvider
```

3. Use in `main.py`:

```python
from windows_use.llms.your_provider import ChatYourProvider

llm = ChatYourProvider(model="model-name", api_key=api_key)
agent = Agent(llm=llm)
```

### Message Serialization

Each provider must handle 4 message types:

```python
def serialize_messages(self, messages: list) -> list:
    serialized = []
    for msg in messages:
        if isinstance(msg, SystemMessage):
            serialized.append({"role": "system", "content": msg.content})
        elif isinstance(msg, HumanMessage):
            serialized.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            serialized.append({"role": "assistant", "content": msg.content})
        elif isinstance(msg, ImageMessage):
            # Handle image + text
            serialized.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": msg.content},
                    {"type": "image", "source": msg.image_to_base64()}
                ]
            })
    return serialized
```

---

## Event System

### Event Architecture

Windows-Use monitors UI events via Windows UI Automation COM interfaces:

```
┌─────────────────────────────────┐
│  WatchDog Service               │
├─────────────────────────────────┤
│  ├─ FocusChangedEventHandler    │ → _on_focus_change callback
│  ├─ StructureChangedEventHandler│ → _on_structure_change callback
│  └─ PropertyChangedEventHandler │ → _on_property_change callback
└─────────────────────────────────┘
         ↓
    COM Event Listeners (STA Thread)
         ↓
┌─────────────────────────────────┐
│  Callbacks (Desktop.tree)       │
│  ├─ Focus updates              │
│  ├─ Tree reconstruction        │
│  └─ Property changes           │
└─────────────────────────────────┘
```

### WatchDog Usage

```python
with self.watchdog:
    # Register callbacks
    self.watchdog.set_focus_callback(self.desktop.tree._on_focus_change)
    self.watchdog.set_structure_callback(self.desktop.tree._on_structure_change)
    self.watchdog.set_property_callback(self.desktop.tree._on_property_change)

    # Event monitoring active
    # Callbacks triggered automatically on UI changes
```

### Event Types (36 documented in `windows_use/uia/events.py`)

**Window Events**:
- `UIA_Window_WindowOpenedEventId` (20016)
- `UIA_Window_WindowClosedEventId` (20017)

**Focus Events**:
- `UIA_AutomationFocusChangedEventId` (20005)

**Structure Events**:
- `UIA_StructureChangedEventId` (20002)
- Change types: Added, Removed, Invalidated, Reordered, PropertyChanged

**Property Events**:
- `UIA_AutomationPropertyChangedEventId` (20004)

### Event Handler Implementation

```python
class MyEventHandler:
    def __init__(self, parent):
        self.parent = parent

    def HandleEvent(self, sender, event_args):
        """COM interface method."""
        # Process event
        if self.parent._callback:
            self.parent._callback(sender, event_args)
        return 0  # S_OK
```

### Runtime ID Tracking

Elements are identified by COM `RuntimeId` (tuple of ints):
- Unique identifier for each control
- Persists across UI updates
- Used to match controls pre/post event

---

## Security Considerations

### Critical Security Warnings

⚠️ **Windows-Use has NO sandbox or isolation layer**

The agent can:
- Delete files or folders
- Modify system configurations
- Install/uninstall software
- Access sensitive data
- Execute potentially harmful commands
- Make irreversible changes

### Development Best Practices

#### 1. Always Use Isolation
```
✅ Virtual Machine (VirtualBox, VMware, Hyper-V)
✅ Windows Sandbox (Windows 10/11 Pro/Enterprise)
✅ Dedicated test machine
❌ Never use on production systems
❌ Never use on your primary work machine
```

#### 2. Input Validation
When adding new tools:

```python
@Tool(name="my_tool", ...)
def my_tool(file_path: str):
    # GOOD: Validate input
    if not os.path.exists(file_path):
        raise ValueError(f"File not found: {file_path}")

    # GOOD: Sanitize paths
    safe_path = os.path.normpath(file_path)
    if ".." in safe_path:
        raise ValueError("Path traversal detected")

    # BAD: No validation
    os.remove(file_path)  # Dangerous!
```

#### 3. Sensitive Data
```python
# NEVER commit:
- API keys
- Credentials
- Tokens
- .env files with secrets

# Use environment variables:
import os
api_key = os.getenv("ANTHROPIC_API_KEY")
```

#### 4. Shell Command Safety

```python
# GOOD: Whitelist safe commands
SAFE_COMMANDS = ["dir", "echo", "type"]

def shell_tool(command: str):
    cmd_name = command.split()[0].lower()
    if cmd_name not in SAFE_COMMANDS:
        logger.warning(f"Potentially unsafe command: {command}")
    # Execute with caution

# BAD: Execute without validation
subprocess.run(command, shell=True)  # Dangerous!
```

### Security Checklist for Contributors

- [ ] Never commit credentials or API keys
- [ ] Review code for potential security issues
- [ ] Test changes in an isolated environment
- [ ] Document security implications of new features
- [ ] Follow secure coding practices
- [ ] Consider principle of least privilege
- [ ] Add appropriate warnings to documentation

### Reporting Security Vulnerabilities

**DO NOT** open public GitHub issues for security vulnerabilities.

Email: jeogeoalukka@gmail.com

---

## Common Tasks & Patterns

### Task 1: Adding a New Tool

**Steps**:

1. **Define Pydantic Schema** (`windows_use/agent/tools/views.py`):
```python
class MyToolInput(BaseModel):
    param1: str = Field(..., description="Description")
    param2: int = Field(default=0, description="Description")
```

2. **Implement Tool Function** (`windows_use/agent/tools/service.py`):
```python
@Tool(
    name="my_tool",
    description="What this tool does and when to use it",
    args_schema=MyToolInput
)
def my_tool(param1: str, param2: int = 0) -> str:
    """Implementation.

    Args:
        param1: Description
        param2: Description

    Returns:
        Success/failure message
    """
    # Implementation
    return "Success"
```

3. **Export Tool** (`windows_use/agent/tools/__init__.py`):
```python
from windows_use.agent.tools.service import my_tool
```

4. **Register in Agent** (`windows_use/agent/service.py`):
```python
self.registry = Registry([
    click_tool, type_tool, ...,
    my_tool  # Add here
])
```

5. **Write Tests** (`tests/unit/agent/agent_tools/test_agent_tools_service.py`):
```python
def test_my_tool():
    result = my_tool(param1="test", param2=42)
    assert "Success" in result
```

### Task 2: Modifying UI Element Classification

**Location**: `windows_use/agent/tree/config.py`

**Example**: Add new control type to interactive elements

```python
INTERACTIVE_CONTROL_TYPE_NAMES = {
    "ButtonControl",
    "EditControl",
    "MyNewControlType",  # Add here
    # ...
}
```

**Remember**: Also update `INFORMATIVE_CONTROL_TYPE_NAMES` if needed to avoid conflicts.

### Task 3: Updating Prompt Templates

**Location**: `windows_use/agent/prompt/*.md`

**Example**: Modify system prompt

1. Edit `windows_use/agent/prompt/system.md`:
```markdown
<new_section>
Additional instructions for the agent.
</new_section>
```

2. Update `Prompt.system_prompt()` if new variables needed:
```python
def system_prompt(desktop, browser, language, instructions, tools_prompt, max_steps):
    # Read template
    template = read_file("system.md")
    # Add new variable substitution
    return template.replace("{new_var}", new_value)
```

### Task 4: Adding Event Callbacks

**Example**: Add custom event handler

1. **Define Callback** (`windows_use/agent/tree/service.py`):
```python
def _on_my_event(self, sender, event_args):
    """Handle my custom event."""
    logger.info(f"Custom event triggered: {sender}")
    # Process event
```

2. **Register Callback** (`windows_use/agent/service.py`):
```python
self.watchdog.set_my_callback(self.desktop.tree._on_my_event)
```

3. **Implement Handler** (`windows_use/agent/watchdog/service.py`):
```python
class MyEventHandler:
    def __init__(self, parent):
        self.parent = parent

    def HandleMyEvent(self, sender, event_args):
        if self.parent._my_callback:
            self.parent._my_callback(sender, event_args)
        return 0
```

### Task 5: Debugging Agent Loop

**Enable Debug Logging**:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Add Custom Logging**:

```python
logger.debug(f"[Agent] Current step: {self.agent_step.steps}")
logger.debug(f"[Desktop] Active app: {active_app.name}")
logger.debug(f"[Tree] Found {len(interactive)} interactive elements")
```

**Inspect State**:

```python
# In agent loop
desktop_state = self.desktop.get_state(use_vision=False)
print(f"Apps: {len(desktop_state.apps)}")
print(f"Interactive elements: {len(desktop_state.tree.interactive)}")
print(f"Cursor: {desktop_state.cursor}")
```

---

## Troubleshooting

### Common Issues

#### 1. COM Initialization Errors

**Problem**: `CoInitialize has not been called`

**Solution**: Ensure COM is initialized in thread:
```python
import pythoncom
pythoncom.CoInitialize()
try:
    # COM operations
finally:
    pythoncom.CoUninitialize()
```

#### 2. Element Not Found

**Problem**: Agent can't find UI element

**Debug Steps**:
1. Check if element is visible: `is_element_visible(element)`
2. Check if element is interactive: control type in `INTERACTIVE_CONTROL_TYPE_NAMES`
3. Verify element is not off-screen
4. Check if window is minimized

**Solution**:
```python
# Add debug logging in tree service
logger.debug(f"Element: {element.Name}, Visible: {is_visible}, Type: {element.ControlType}")
```

#### 3. LLM Response Parsing Errors

**Problem**: `extract_agent_data()` fails to parse LLM response

**Debug**:
```python
# Add logging in utils.py
logger.debug(f"Raw LLM response: {response}")
logger.debug(f"Extracted action: {action_name}")
logger.debug(f"Extracted input: {action_input}")
```

**Solution**: Ensure LLM follows XML output format:
```xml
<output>
  <evaluate>Success | Neutral | Fail</evaluate>
  <thought>Reasoning</thought>
  <action_name>tool_name</action_name>
  <action_input>{"param": "value"}</action_input>
</output>
```

#### 4. Screenshot/Vision Issues

**Problem**: Annotated screenshot not generating

**Debug**:
```python
# Check if Pillow is installed
from PIL import Image
# Check if screenshot is captured
screenshot = pyautogui.screenshot()
screenshot.save("debug.png")
```

**Solution**: Ensure `use_vision=True` and PIL is installed:
```bash
pip install pillow
```

#### 5. Memory Tool File Errors

**Problem**: Can't read/write memory files

**Debug**:
```python
import os
memory_dir = ".memories"
print(f"Memory dir exists: {os.path.exists(memory_dir)}")
print(f"Files: {os.listdir(memory_dir)}")
```

**Solution**: Ensure `.memories` directory exists and has write permissions:
```python
os.makedirs(".memories", exist_ok=True)
```

#### 6. Threading/Parallel Processing Errors

**Problem**: `ThreadPoolExecutor` failures

**Debug**:
```python
# Add exception handling in futures
for future in as_completed(futures):
    try:
        result = future.result()
    except Exception as e:
        logger.error(f"Thread failed: {e}")
```

**Solution**: Increase retry count or add error handling:
```python
# In tree/config.py
THREAD_MAX_RETRIES = 5  # Increase from 3
```

### Performance Optimization

#### 1. Reduce Element Count
```python
# Filter more aggressively in tree service
min_visible_area = 0.5  # Increase threshold
```

#### 2. Disable Vision
```python
# Vision adds overhead
agent = Agent(llm=llm, use_vision=False)
```

#### 3. Limit Max Steps
```python
# Reduce max steps for faster iteration
agent = Agent(llm=llm, max_steps=15)  # Default: 25
```

#### 4. Use Local LLM
```python
# Faster response with Ollama
from windows_use.llms.ollama import ChatOllama
llm = ChatOllama(model="llama3")
```

---

## Quick Reference

### Important File Paths
```
windows_use/agent/service.py                 # Main agent loop
windows_use/agent/desktop/service.py         # Desktop management
windows_use/agent/tree/service.py            # UI tree extraction
windows_use/agent/tools/service.py           # Tool implementations
windows_use/agent/registry/service.py        # Tool registry
windows_use/agent/watchdog/service.py        # Event monitoring
windows_use/llms/base.py                     # LLM protocol
windows_use/uia/core.py                      # Windows UIA wrapper
```

### Key Configuration Files
```
windows_use/agent/desktop/config.py          # Browser names, excluded apps
windows_use/agent/tree/config.py             # Control type classifications
windows_use/agent/prompt/system.md           # System prompt template
pyproject.toml                               # Project config, dependencies
```

### Important Constants
```python
THREAD_MAX_RETRIES = 3                       # tree/config.py
BROWSER_NAMES = {...}                        # desktop/config.py
INTERACTIVE_CONTROL_TYPE_NAMES = {...}       # tree/config.py
PROCESS_PER_MONITOR_DPI_AWARE = 2           # desktop/config.py
```

### Useful Commands
```bash
# Run agent
uv run main.py

# Run tests
pytest

# Format code
ruff format windows_use/

# Check linting
ruff check windows_use/

# Install pre-commit
pre-commit install

# Run pre-commit manually
pre-commit run --all-files
```

---

## Additional Resources

- **README.md**: Project overview and installation
- **CONTRIBUTING.md**: Detailed contribution guidelines
- **SECURITY.md**: Security policy and best practices
- **AGENTS.md**: Agent capabilities and usage
- **GitHub**: https://github.com/CursorTouch/Windows-Use
- **Discord**: https://discord.com/invite/Aue9Yj2VzS
- **Twitter**: https://x.com/CursorTouch

---

## Changelog

### Version 0.7.0 (Current)
- **Performance Optimization**: Introduced UIA caching for 10x faster tree traversal.
- **Virtual Desktop Support**: New `vdm` module and `desktop_tool` for workspace management.
- **Multi-screen Support**: Enhanced capabilities for multiple monitors.
- **Annotation Support**: Added manual control over annotated screenshots.
- **Tool improvements**: Unified `move_tool` to handle both movement and dragging.
- **Stability**: Fixed memory leaks in COM event handlers.

### Version 0.6.9
- Migrated from langchain/langgraph
- Event handling system implemented
- Structure change callbacks added
- Property change monitoring
- Focus tracking improvements

### Future Enhancements
- Action allowlisting/blocklisting
- Dry-run mode
- Rollback capabilities
- Enhanced logging
- Security monitoring integration

---

**For AI Assistants**: This document should be your primary reference when working on the Windows-Use codebase. Always consult this guide before making architectural decisions, adding features, or modifying core components. When in doubt, follow the patterns established here and maintain consistency with existing code.
