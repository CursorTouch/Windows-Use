import pytest
from typing import Callable
from unittest.mock import MagicMock

from windows_use.agent.registry.views import Tool, ToolResult

class TestAgentRegistryViews:
    """
    Tests for the data models in windows_use.agent.registry.views.
    """

    def test_tool_initialization(self):
        """
        Test Tool initialization.

        What is being tested:
            - `name`, `description`, `function`, and `params` are set correctly.
        """
        mock_function = MagicMock(spec=Callable)
        tool = Tool(
            name="TestTool",
            description="A test tool",
            function=mock_function,
            params={"param1": "value1"},
        )
        assert tool.name == "TestTool"
        assert tool.description == "A test tool"
        assert tool.function == mock_function
        assert tool.params == {"param1": "value1"}

    @pytest.mark.parametrize(
        "is_success, content, error",
        [
            (True, "Operation successful", None),
            (False, None, "Operation failed"),
            (True, None, None),  # Valid for success with no content
            (False, "Partial content", "Error occurred"), # Content and error can coexist
        ],
    )
    def test_tool_result_initialization(self, is_success, content, error):
        """
        Test ToolResult initialization with various combinations of success, content, and error.

        What is being tested:
            - `is_success`, `content`, and `error` are set correctly based on input.
        """
        result = ToolResult(is_success=is_success, content=content, error=error)
        assert result.is_success == is_success
        assert result.content == content
        assert result.error == error
