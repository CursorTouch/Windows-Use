# tests/unit/agent/agent_registry/test_agent_registry_views.py

import pytest
from windows_use.agent.registry.views import ToolResult

class TestAgentRegistryViews:
    """
    Tests for the data models in windows_use.agent.registry.views.
    """

    @pytest.mark.parametrize(
        "is_success, content, error",
        [
            (True, "Operation successful", None),
            (False, None, "Operation failed"),
            (True, None, None),
            (False, "Partial content", "Error occurred"),
        ],
    )
    def test_tool_result_initialization(self, is_success, content, error):
        """
        Test ToolResult initialization.
        """
        result = ToolResult(is_success=is_success, content=content, error=error)
        assert result.is_success == is_success
        assert result.content == content
        assert result.error == error
