import pytest
from unittest.mock import ANY
from textwrap import dedent

# --- Import classes to be tested and mocked ---
from windows_use.agent.registry.service import Registry
from windows_use.agent.registry.views import Tool as ToolData, ToolResult
from windows_use.desktop.service import Desktop
from langchain.tools import Tool as LangchainTool


# #############################################################################
# Fixtures: The foundation of the test suite.
# #############################################################################

@pytest.fixture
def mock_langchain_tool(mocker):
    """Provides a high-fidelity mock of a LangchainTool instance."""

    # 1. Create the mock instance first using autospec.
    #    This ensures it has the same methods as the real LangchainTool.
    mock_tool = mocker.create_autospec(LangchainTool, instance=True)

    # 2. Now, explicitly set the attributes that the production code will access.
    #    autospec will allow this because the real LangchainTool has these attributes.
    mock_tool.name = "TestTool"
    mock_tool.description = "A test tool description."
    mock_tool.args = {"param1": {"type": "str"}}
    
    # 3. Configure the mock's behavior.
    mock_tool.run.return_value = "Tool executed successfully"
    
    return mock_tool

@pytest.fixture
def mock_desktop(mocker):
    """Provides a high-fidelity mock of a Desktop instance."""
    return mocker.create_autospec(Desktop, instance=True)

@pytest.fixture
def registry_instance(mock_langchain_tool):
    """Provides a pre-initialized Registry instance for tests."""
    return Registry(tools=[mock_langchain_tool])


# #############################################################################
# Test Class
# #############################################################################

class TestRegistry:
    """Tests for the Registry service class."""

    def test_init(self, registry_instance, mock_langchain_tool):
        """
        Tests that the Registry initializes correctly, creating ToolData objects.
        """
        # Assert
        assert registry_instance.tools == [mock_langchain_tool]
        assert "TestTool" in registry_instance.tools_registry

        tool_data = registry_instance.tools_registry["TestTool"]
        assert isinstance(tool_data, ToolData)
        assert tool_data.name == "TestTool"
        assert tool_data.description == "A test tool description."
        assert tool_data.params == {"param1": {"type": "str"}}
        assert tool_data.function == mock_langchain_tool.run

    def test_get_tools_prompt(self, registry_instance):
        """
        Tests that the combined prompt for all tools is generated correctly.
        """
        # Act
        prompt = registry_instance.get_tools_prompt()

        # Assert
        # Using .strip() to handle potential leading/trailing whitespace from dedent
        expected = dedent("""
        Available Tools:

        Tool Name: TestTool
        Description: A test tool description.
        Parameters: {'param1': {'type': 'str'}}
        """).strip()
        assert prompt.strip() == expected
    
    @pytest.mark.parametrize(
        "tool_name, expected_output_contains",
        [
            ("TestTool", "Tool Name: TestTool"),
            ("NonExistentTool", "Tool 'NonExistentTool' not found."),
        ],
        ids=["Tool Found", "Tool Not Found"]
    )
    def test_tool_prompt(self, registry_instance, tool_name, expected_output_contains):
        """
        Tests `tool_prompt` for both found and not-found cases.
        """
        # Act
        prompt = registry_instance.tool_prompt(tool_name)

        # Assert
        assert expected_output_contains in prompt

    @pytest.mark.parametrize(
        "tool_name, tool_kwargs, run_side_effect, expected_result",
        [
            pytest.param(
                "TestTool",
                {"param1": "value1"},
                None,  # No exception
                ToolResult(is_success=True, content="Tool executed successfully"),
                id="Success"
            ),
            pytest.param(
                "TestTool",
                {"param1": "value1"},
                ValueError("Something went wrong"),  # An exception is raised
                ToolResult(is_success=False, error="Something went wrong"),
                id="Execution Failure (Exception)"
            ),
            pytest.param(
                "NonExistentTool",
                {},
                None,
                ToolResult(is_success=False, error="Tool 'NonExistentTool' not found."),
                id="Tool Not Found"
            ),
        ]
    )
    def test_execute(self, registry_instance, mock_langchain_tool, mock_desktop, tool_name, tool_kwargs, run_side_effect, expected_result):
        """
        Tests all execution paths of the `execute` method.
        """
        # Arrange
        mock_langchain_tool.run.side_effect = run_side_effect
        
        # Act
        result = registry_instance.execute(tool_name, desktop=mock_desktop, **tool_kwargs)
        
        # Assert
        assert result == expected_result
        
        # Also assert the mock was called correctly if the tool was supposed to be found
        if tool_name == "TestTool":
            expected_tool_input = {"desktop": mock_desktop} | tool_kwargs
            mock_langchain_tool.run.assert_called_once_with(tool_input=expected_tool_input)
        else:
            mock_langchain_tool.run.assert_not_called()