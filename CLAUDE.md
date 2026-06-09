# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Windows-Use** is an AI agent that controls Windows at the GUI layer using the Windows UI Automation API. It detects clickable elements on screen, reads application state, and executes actions (click, type, scroll, drag, PowerShell commands) based on LLM decisions.

The agent works without computer vision — it reads the accessibility tree and uses any multi-provider LLM (Anthropic, OpenAI, Google, Ollama, etc.) to decide what actions to take.

## Architecture

Windows-Use has three main layers that interact vertically:

### 1. **Engine** (`windows_use/engine/`)
- Re-exports types and services from Operator-Use's LLM streaming engine
- Handles raw streaming loop, tool execution, and abort signals
- Imports from `operator_use.engine.*` (external dependency)
- Windows-Use treats this as a sealed interface — do not modify engine behavior, work through Desktop/tool definitions instead

### 2. **Computer** (`windows_use/computer/`)
The Windows-specific automation layer split across three modules:

**Desktop** (`computer/desktop/`)
- Main service (`Desktop` class) that owns the entire Windows automation surface
- Exposes methods: `click()`, `type()`, `drag()`, `scroll()`, `app()`, `execute_command()`, `get_state()`
- Caches window state and screen annotations
- Manages browser selection (Chrome, Edge, Firefox, Safari)
- Returns `DesktopState` with current windows, active window, and visual tree

**Tree** (`computer/tree/`)
- UI Automation tree traversal via comtypes + Windows UIA API
- Extracts interactive and scrollable elements from the current window tree
- Returns `TreeState` with `interactive_nodes`, `scrollable_nodes`, and `dom_informative_nodes`
- Handles browser-specific DOM extraction for web page scraping
- Caches control objects to avoid redundant COM calls

**Watchdog** (`computer/watchdog/`)
- Monitors window focus, creation, and destruction events
- Debounces duplicate focus events
- Used for reactive agent logic (not core automation)

### 3. **UIA** (`windows_use/uia/`)
- Thin wrapper around Windows UI Automation COM API via comtypes
- Exposes Control, Rect, Pattern objects and enumerations
- Handles COM marshaling and exception translation
- Do not call into this directly from agents — always go through Desktop or Tree

## Common Development Tasks

### Build and Install
```bash
# Using uv (preferred)
uv sync
uv build

# Using pip
pip install -e .

# Install with dev dependencies
uv sync --group dev
```

### Run Tests
```bash
# All tests
pytest

# Single test file
pytest tests/unit/test_imports.py

# Single test function
pytest tests/unit/test_imports.py::test_something

# With verbose output
pytest -v

# Show print statements
pytest -s
```

### Lint and Format
```bash
# Lint check (ruff)
ruff check .

# Auto-fix linting issues
ruff check . --fix

# Format code
ruff format .

# Both in one (pre-commit does this)
pre-commit run --all-files
```

### Type Checking
```bash
# Windows-Use does not have pyright configured yet
# But the engine module uses operator_use.engine types
# Type hints are optional but strongly encouraged for public APIs
```

### Development Flow
1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes, run tests: `pytest`
3. Fix lint: `ruff check . --fix && ruff format .`
4. Commit: `git commit -m "message"`
5. Push and create PR

## Key Invariants

Violating these breaks the agent:

- **Desktop is the single source of truth.** Everything goes through `Desktop.get_state()` for screen state. Never cache window positions or element references across calls — UI Automation elements are ephemeral COM objects.
- **Element handles are short-lived.** Control objects from `tree.interactive_nodes` are only valid within that `get_state()` call. The next call to `get_state()` invalidates all controls. Store indices (`SelectorMap`), not Control objects.
- **Tree traversal is one-shot.** `Tree.get_state(active_handle, other_handles)` walks the tree and returns everything at once. It does not maintain state between calls.
- **Metadata is for enrichment only.** Element metadata (has_focused, shortcut, toggle_state, etc.) is stored as dicts and serialized to JSON in tree output. Do not treat it as a strict schema — new metadata fields can be added without breaking consumers.
- **Windows-Use delegates engine behavior.** The LLM inference loop, context compaction, retry logic, and session persistence are handled by Operator-Use's Engine. Do not duplicate that logic here.

## Code Organization Reference

| Path | Purpose |
|------|---------|
| `windows_use/computer/desktop/` | Desktop service, window/app control |
| `windows_use/computer/tree/` | UI Automation tree extraction |
| `windows_use/computer/watchdog/` | Window event monitoring |
| `windows_use/uia/` | UI Automation COM wrapper |
| `windows_use/engine/` | Engine re-exports (sealed, from Operator-Use) |
| `windows_use/vdm/` | Virtual Desktop Manager (Win 10+) |
| `windows_use/providers/` | LLM provider integrations |
| `tests/` | Unit and integration tests |
| `docs/` | Auto-generated Windows API reference |

## Important Files

- **`pyproject.toml`** — Dependency list, build config, ruff settings, pytest config
- **`.pre-commit-config.yaml`** — Git hooks: ruff lint/format on commit
- **`.gitignore`** — Standard Python + Windows paths
- **`README.md`** — User-facing quickstart and feature list
- **`uv.lock`** — Locked dependency versions (check in to git)

## Integration Points

When adding new functionality:

1. **New Desktop methods** → Add to `Desktop` class, update `get_state()` if needed
2. **New tree metadata** → Add to `TreeElementNode.metadata` dict or `ScrollElementNode.metadata`
3. **New LLM provider** → Create `windows_use/providers/yourprovider/llm.py` inheriting from base
4. **New tool for agents** → Define in agent tools module (not yet fully structured; check Operator-Use's pattern)

## Engine / Operator-Use Dependency

Windows-Use depends on Operator-Use's Engine:
- Imports: `from operator_use.engine.*` and `from operator_use.tool.*`
- The Engine is sealed here — it is a stable interface
- If Engine needs Windows-specific changes, raise them in Operator-Use, not here
- Windows-Use adds Windows desktop control *on top* of the Engine's tool execution, not inside it

## Testing Strategy

- **Unit tests** (`tests/unit/`) — test individual modules in isolation (mock Desktop, Tree)
- **Integration tests** (`tests/`) — test actual UIA and desktop control (slow, Windows-only)
- Use pytest fixtures for common mock objects (mock_desktop, sample_tree_state, etc.)
- Do not test third-party libraries (PIL, comtypes, win32gui) — assume they work

## Troubleshooting

**"COM object is no longer valid"** → You're holding a Control object across a `get_state()` call. Get the index from `SelectorMap` and re-fetch the Control in the next state.

**"No elements found"** → Tree traversal succeeded but UIA found no interactive controls. This is normal for some apps. Use vision mode or manual clicks as fallback.

**"UIAException: element doesn't support pattern"** → Element doesn't have the requested Pattern (e.g., ScrollPattern on a Button). Check control type before accessing patterns.

**Type errors for scroll metadata** → Scroll properties (horizontal_scrollable, etc.) are in `ScrollElementNode.metadata`, not direct fields.
