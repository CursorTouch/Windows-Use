# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.7.66] - 2026-03-25

### Added
- **Telemetry**: Agent now sends structured `agent_event` data to PostHog on every `invoke`/`ainvoke` call, capturing query, steps, model, provider, success/failure, and error details. Runs silently with no console output.
- **Public API**: `Agent`, `Browser`, `AgentEvent`, `EventType`, `BaseEventSubscriber` and friends are now importable directly from `windows_use` — `from windows_use import Agent, Browser`.
- **CI/CD**: GitHub Actions workflows for linting (ruff via pre-commit) and tests on Windows across Python 3.10–3.13, plus automated PyPI publishing on version tags.

### Fixed
- **Tree traversal**: `NoneType.strip()` crashes when Windows UI Automation returns `None` for element names — fixed with `(value or '').strip()` in 6 locations.
- **Event system**: `ValueError: list.remove(x): x not in list` when removing an event subscriber that was already removed or never added.
- **Telemetry user ID**: `PermissionError` on systems where `TEMP` points to `C:\WINDOWS\TEMP` — now uses `tempfile.gettempdir()`.

## [0.7.4] - 2026-01-30

### Changed
- **Performance Optimization**: 
  - Significant improvement in **Tree Traversal speed** (0.2-0.8s).
  - **Desktop State Capture** optimized to (0.4-1.0s).
  - Reduced computation expense by removing reliance on the root level children.
  - Minimized COM calls to **UIA3** using enhanced caching mechanisms.
- **LLM Wrappers**:
  - Updated LLM wrappers for better reliability.
  - Implemented Minimal Schema for Ollama to reduce token usage and improve stability.

### Fixed
- **VDM**: Fixes for Virtual Desktop Manager interaction.


## [0.7.1] - 2026-01-27

### Added
- **Windows 11 Support**: Updated VDM to support Windows 11 Build 26100.4349.
- **Ollama**: Added schema sanitization for Ollama.

### Fixed
- **Tool Schema**: Updated tool schema generation to resolve understanding issues for some models.
- **Vision**: Minor fixes to the vision capabilities in LLM wrappers.

## [0.7.0] - 2026-01-21

### Added
- **Multi-screen Support**: Enhanced capabilities to interact with multiple monitors.
- **Desktop Tool**: New tool for Windows 10/11 users to enable desktop switching, creation, and deletion.
- **Annotation Support**: Added `use_annotation` parameter in the agent to allow requesting plain or annotated screenshots.

### Changed
- **Performance Optimization**: Introduced caching to significantly speed up tree traversal.
- **Resource Usage**: Reduced usage of the UIA module for app retrieval to enhance desktop state speed.
- **Tool Merging**: Merged `drag_tool` and `move_tool` into a single, unified `move_tool`.

### Fixed
- **Memory Leaks**: Fixed memory leaks in the system to improve stability.
