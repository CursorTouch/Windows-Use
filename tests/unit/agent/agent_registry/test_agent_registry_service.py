# tests/unit/agent/agent_registry/test_agent_registry_service.py

import pytest
from unittest.mock import MagicMock
from windows_use.agent.registry.service import Registry
from windows_use.agent.registry.views import ToolResult
from windows_use.tools import Tool

class TestRegistry:
    """Tests for the Registry service class."""

    @pytest.fixture
    def mock_tool(self):
        """Provides a mock Tool instance."""
        mock = MagicMock(spec=Tool)
        mock.name = "TestTool"
        mock.json_schema = {"name": "TestTool", "parameters": {}}
        mock.validate.return_value = [] # No errors
        mock.invoke.return_value = "Tool execution result"
        return mock

    def test_init(self, mock_tool):
        """Test Registry initialization."""
        registry = Registry(tools=[mock_tool])
        assert registry.tools == [mock_tool]
        assert "TestTool" in registry.tools_registry
        assert registry.tools_registry["TestTool"] == mock_tool

    def test_get_tools_schema(self, mock_tool):
        """Test get_tools_schema method."""
        registry = Registry(tools=[mock_tool])
        schema = registry.get_tools_schema()
        assert schema == [{"name": "TestTool", "parameters": {}}]

    def test_execute_success(self, mock_tool):
        """Test successful tool execution."""
        registry = Registry(tools=[mock_tool])
        mock_desktop = MagicMock()
        
        result = registry.execute("TestTool", desktop=mock_desktop, param1="val1")
        
        assert result.is_success is True
        assert result.content == "Tool execution result"
        mock_tool.invoke.assert_called_once_with(desktop=mock_desktop, param1="val1")

    def test_execute_validation_failure(self, mock_tool):
        """Test tool execution with validation failure."""
        mock_tool.validate.return_value = ["Invalid param"]
        registry = Registry(tools=[mock_tool])
        
        result = registry.execute("TestTool", param1="val1")
        
        assert result.is_success is False
        assert "validation failed" in result.error
        mock_tool.invoke.assert_not_called()

    def test_execute_not_found(self):
        """Test execution of non-existent tool."""
        registry = Registry(tools=[])
        result = registry.execute("NonExistent")
        assert result.is_success is False
        assert "not found" in result.error