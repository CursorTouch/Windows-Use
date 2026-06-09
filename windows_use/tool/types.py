from __future__ import annotations
import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Awaitable, Callable, Optional, Type
from windows_use.computer.desktop import Desktop
from windows_use.inference import LLM
from pydantic import BaseModel

@dataclass
class ToolError:
    """File-level tool load failure with optional stack trace."""
    path: str
    error: str
    stack: str = ''


@dataclass
class LoadToolsResult:
    """Aggregate result of loading tools from one or more directories."""

    tools: list[Tool] = field(default_factory=list)
    errors: list[ToolError] = field(default_factory=list)


class ToolExecutionMode(str, Enum):
    """Controls how the engine schedules concurrent calls to the same tool."""

    Sequential = "sequential"
    Parallel = "parallel"
    Batch = "batch"


@dataclass
class ToolInvocation:
    """Complete tool call specification with resolved args and execution context."""
    id: str
    params: dict[str, Any] = field(default_factory=dict)
    cwd: str = ""
    name: str = ""

@dataclass
class ToolContext:
    desktop:Desktop
    llm: LLM


@dataclass
class ToolResult:
    """Tool execution outcome with optional error flag and early termination signal."""
    id: str
    content: str
    is_error: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)
    terminate: bool = False
    terminate_message: str | None = None

    @classmethod
    def ok(
        cls,
        id: str,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> ToolResult:
        """Construct a successful outcome.

        Args:
            id: The tool call ID this result corresponds to.
            content: The result content (output of the tool).
            metadata: Optional metadata dict (default empty).

        Returns:
            A ToolResult with is_error=False.
        """
        return cls(id=id, content=content, is_error=False, metadata=metadata or {})

    @classmethod
    def error(
        cls,
        id: str,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> ToolResult:
        """Construct a failed outcome.

        Args:
            id: The tool call ID this result corresponds to.
            content: The error message or description.
            metadata: Optional metadata dict (default empty).

        Returns:
            A ToolResult with is_error=True.
        """
        return cls(id=id, content=content, is_error=True, metadata=metadata or {})

ToolExecutionUpdateCallback = Callable[[ToolResult], Awaitable[None]]

AbortSignal = asyncio.Event

class Tool(ABC):
    """Abstract base for tools: executable, schema-validated components with metadata and policy."""
    def __init__(
        self,
        name: str,
        description: str,
        schema: Type[BaseModel],
        execution_mode: ToolExecutionMode = ToolExecutionMode.Sequential,
        display_name: str = "",
    ) -> None:
        """Initialize tool with name, description, schema, kind, and execution concurrency policy."""
        self.name = name
        self.description = description
        self.schema = schema
        self.execution_mode = execution_mode
        self.display_name = display_name

    def get_display_name(self, args: dict[str, Any]) -> str:
        """Return a human-readable channel label based on call args; override for intent-specific messages.

        Falls back to display_name then name when not overridden.

        Args:
            args: Tool call parameters; may be used to generate context-specific labels.

        Returns:
            A human-readable label for the tool call.
        """
        return self.display_name or self.name

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate params against schema; return (success, error_list).

        Args:
            params: Tool call parameters to validate.

        Returns:
            A tuple of (success: bool, errors: list[str]).
        """
        try:
            self.schema.model_validate(params)
            return True, []
        except Exception as e:
            from pydantic import ValidationError
            # Format Pydantic errors with field path for clarity
            if isinstance(e, ValidationError):
                errors = [
                    f"{' -> '.join(str(loc) for loc in err['loc'])}: {err['msg']}"
                    for err in e.errors()
                ]
            else:
                errors = [str(e)]
            return False, errors

    def to_json(self) -> dict[str, Any]:
        """Serialize to JSON schema with name, description, and input_schema.

        Returns:
            A dict with 'name', 'description', and 'input_schema' keys suitable for provider APIs.
        """
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.schema.model_json_schema(),
        }

    def _is_cancelled(self, signal: Optional[AbortSignal]) -> bool:
        """Check if abort signal has been set.

        Args:
            signal: Optional asyncio.Event abort signal.

        Returns:
            True if the signal has been set, indicating cancellation requested.
        """
        return signal is not None and signal.is_set()

    @abstractmethod
    async def execute(
        self,
        invocation: ToolInvocation,
        tool_execution_update_callback: Optional[ToolExecutionUpdateCallback] = None,
        signal: Optional[AbortSignal] = None,
    ) -> ToolResult:
        """Execute the tool with params; subclasses must override.

        Args:
            invocation: Complete tool call specification with resolved parameters.
            tool_execution_update_callback: Optional callback for streaming updates.
            signal: Optional abort signal to check for user-initiated cancellation.
            context: Optional ToolContext with runtime services available to the tool.

        Returns:
            A ToolResult with the outcome, content, and optional error details.
        """
        ...
