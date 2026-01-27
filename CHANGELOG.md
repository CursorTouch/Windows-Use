# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
