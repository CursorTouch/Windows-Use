"""Custom exception classes for Windows-Use."""

from typing import Any, Optional


class WindowsUseError(Exception):
    """Base exception class for all Windows-Use errors."""

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        if self.details:
            details_str = ", ".join(f"{k}={v}" for k, v in self.details.items())
            return f"{self.message} ({details_str})"
        return self.message


class LLMError(WindowsUseError):
    """Raised when LLM operations fail."""

    def __init__(
        self,
        message: str,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        details = details or {}
        if provider:
            details["provider"] = provider
        if model:
            details["model"] = model
        super().__init__(message, details)


class DesktopInteractionError(WindowsUseError):
    """Raised when desktop interaction operations fail."""

    def __init__(
        self,
        message: str,
        action: Optional[str] = None,
        element: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        details = details or {}
        if action:
            details["action"] = action
        if element:
            details["element"] = element
        super().__init__(message, details)


class ElementNotFoundError(DesktopInteractionError):
    """Raised when a UI element cannot be found."""

    def __init__(
        self,
        element_description: str,
        search_criteria: Optional[dict[str, Any]] = None,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        message = f"Element not found: {element_description}"
        details = details or {}
        if search_criteria:
            details["search_criteria"] = search_criteria
        super().__init__(message, element=element_description, details=details)


class ApplicationError(WindowsUseError):
    """Raised when application operations fail."""

    def __init__(
        self,
        message: str,
        app_name: Optional[str] = None,
        operation: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        details = details or {}
        if app_name:
            details["app_name"] = app_name
        if operation:
            details["operation"] = operation
        super().__init__(message, details)


class ToolExecutionError(WindowsUseError):
    """Raised when tool execution fails."""

    def __init__(
        self,
        message: str,
        tool_name: Optional[str] = None,
        parameters: Optional[dict[str, Any]] = None,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        details = details or {}
        if tool_name:
            details["tool_name"] = tool_name
        if parameters:
            details["parameters"] = parameters
        super().__init__(message, details)


class ConfigurationError(WindowsUseError):
    """Raised when configuration is invalid or missing."""

    def __init__(
        self,
        message: str,
        config_key: Optional[str] = None,
        expected_type: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        details = details or {}
        if config_key:
            details["config_key"] = config_key
        if expected_type:
            details["expected_type"] = expected_type
        super().__init__(message, details)


class MemoryError(WindowsUseError):
    """Raised when memory operations fail."""

    def __init__(
        self,
        message: str,
        operation: Optional[str] = None,
        path: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        details = details or {}
        if operation:
            details["operation"] = operation
        if path:
            details["path"] = path
        super().__init__(message, details)


class ValidationError(WindowsUseError):
    """Raised when input validation fails."""

    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        value: Optional[Any] = None,
        expected: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        details = details or {}
        if field:
            details["field"] = field
        if value is not None:
            details["value"] = value
        if expected:
            details["expected"] = expected
        super().__init__(message, details)


class TimeoutError(WindowsUseError):
    """Raised when operations timeout."""

    def __init__(
        self,
        message: str,
        timeout_seconds: Optional[float] = None,
        operation: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        details = details or {}
        if timeout_seconds:
            details["timeout_seconds"] = timeout_seconds
        if operation:
            details["operation"] = operation
        super().__init__(message, details)


class SecurityError(WindowsUseError):
    """Raised when security constraints are violated."""

    def __init__(
        self,
        message: str,
        action: Optional[str] = None,
        reason: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        details = details or {}
        if action:
            details["action"] = action
        if reason:
            details["reason"] = reason
        super().__init__(message, details)