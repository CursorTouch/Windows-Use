"""Enhanced logging configuration for Windows-Use."""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
from rich.console import Console
from rich.logging import RichHandler
from rich.text import Text


class StructuredFormatter(logging.Formatter):
    """Custom formatter that outputs structured JSON logs."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as structured JSON."""
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields from the record
        for key, value in record.__dict__.items():
            if key not in {
                "name", "msg", "args", "levelname", "levelno", "pathname", 
                "filename", "module", "lineno", "funcName", "created", 
                "msecs", "relativeCreated", "thread", "threadName", 
                "processName", "process", "getMessage", "exc_info", 
                "exc_text", "stack_info"
            }:
                log_data[key] = value

        return json.dumps(log_data, default=str)


class WindowsUseLogger:
    """Enhanced logger for Windows-Use with structured logging and debug modes."""

    def __init__(
        self,
        name: str = "windows_use",
        level: str = "INFO",
        enable_file_logging: bool = True,
        enable_structured_logging: bool = False,
        log_dir: Optional[Path] = None,
    ) -> None:
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        self.console = Console()
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Setup console handler with Rich
        if not enable_structured_logging:
            console_handler = RichHandler(
                console=self.console,
                show_time=True,
                show_path=True,
                markup=True,
                rich_tracebacks=True,
            )
            console_handler.setFormatter(
                logging.Formatter(
                    fmt="%(message)s",
                    datefmt="[%X]",
                )
            )
        else:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(StructuredFormatter())
        
        self.logger.addHandler(console_handler)
        
        # Setup file handler if enabled
        if enable_file_logging:
            log_dir = log_dir or Path.cwd() / "logs"
            log_dir.mkdir(exist_ok=True)
            
            log_file = log_dir / f"{name}.log"
            file_handler = logging.FileHandler(log_file)
            
            if enable_structured_logging:
                file_handler.setFormatter(StructuredFormatter())
            else:
                file_handler.setFormatter(
                    logging.Formatter(
                        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                    )
                )
            
            self.logger.addHandler(file_handler)

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message with optional structured data."""
        self._log_with_extra(logging.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        """Log info message with optional structured data."""
        self._log_with_extra(logging.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message with optional structured data."""
        self._log_with_extra(logging.WARNING, message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        """Log error message with optional structured data."""
        self._log_with_extra(logging.ERROR, message, **kwargs)

    def critical(self, message: str, **kwargs: Any) -> None:
        """Log critical message with optional structured data."""
        self._log_with_extra(logging.CRITICAL, message, **kwargs)

    def _log_with_extra(self, level: int, message: str, **kwargs: Any) -> None:
        """Log message with extra structured data."""
        extra = {k: v for k, v in kwargs.items() if k != "exc_info"}
        self.logger.log(level, message, extra=extra, exc_info=kwargs.get("exc_info"))

    def log_agent_step(
        self,
        step: int,
        action: str,
        thought: str,
        observation: str,
        **kwargs: Any
    ) -> None:
        """Log agent execution step with structured data."""
        self.info(
            f"🎯 Step {step}: {action}",
            step=step,
            action=action,
            thought=thought,
            observation=observation,
            **kwargs
        )

    def log_tool_execution(
        self,
        tool_name: str,
        parameters: Dict[str, Any],
        result: str,
        success: bool,
        execution_time: Optional[float] = None,
        **kwargs: Any
    ) -> None:
        """Log tool execution with structured data."""
        level = logging.INFO if success else logging.ERROR
        status = "✅" if success else "❌"
        
        self._log_with_extra(
            level,
            f"{status} Tool: {tool_name}",
            tool_name=tool_name,
            parameters=parameters,
            result=result,
            success=success,
            execution_time=execution_time,
            **kwargs
        )

    def log_llm_interaction(
        self,
        provider: str,
        model: str,
        prompt_tokens: Optional[int] = None,
        completion_tokens: Optional[int] = None,
        response_time: Optional[float] = None,
        **kwargs: Any
    ) -> None:
        """Log LLM interaction with structured data."""
        self.info(
            f"🤖 LLM: {provider}/{model}",
            provider=provider,
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            response_time=response_time,
            **kwargs
        )

    def log_performance_metric(
        self,
        metric_name: str,
        value: float,
        unit: str = "ms",
        **kwargs: Any
    ) -> None:
        """Log performance metrics."""
        self.info(
            f"📊 {metric_name}: {value}{unit}",
            metric_name=metric_name,
            value=value,
            unit=unit,
            **kwargs
        )

    def log_ui_interaction(
        self,
        action: str,
        element: Optional[str] = None,
        coordinates: Optional[tuple[int, int]] = None,
        success: bool = True,
        **kwargs: Any
    ) -> None:
        """Log UI interaction events."""
        status = "✅" if success else "❌"
        element_info = f" on {element}" if element else ""
        coord_info = f" at {coordinates}" if coordinates else ""
        
        self.info(
            f"{status} UI: {action}{element_info}{coord_info}",
            action=action,
            element=element,
            coordinates=coordinates,
            success=success,
            **kwargs
        )


# Global logger instance
_logger: Optional[WindowsUseLogger] = None


def get_logger(
    name: str = "windows_use",
    level: str = "INFO",
    enable_file_logging: bool = True,
    enable_structured_logging: bool = False,
    log_dir: Optional[Path] = None,
) -> WindowsUseLogger:
    """Get or create the global logger instance."""
    global _logger
    if _logger is None:
        _logger = WindowsUseLogger(
            name=name,
            level=level,
            enable_file_logging=enable_file_logging,
            enable_structured_logging=enable_structured_logging,
            log_dir=log_dir,
        )
    return _logger


def configure_logging(
    level: str = "INFO",
    enable_file_logging: bool = True,
    enable_structured_logging: bool = False,
    log_dir: Optional[Path] = None,
) -> WindowsUseLogger:
    """Configure the global logging system."""
    global _logger
    _logger = WindowsUseLogger(
        level=level,
        enable_file_logging=enable_file_logging,
        enable_structured_logging=enable_structured_logging,
        log_dir=log_dir,
    )
    return _logger