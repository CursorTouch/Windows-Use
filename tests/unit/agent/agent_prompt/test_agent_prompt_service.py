import pytest
from unittest.mock import MagicMock, ANY
from datetime import datetime
from pathlib import Path

# --- The module we are testing ---
from windows_use.agent.prompt.service import Prompt

# --- Import the actual classes to be mocked for autospeccing ---
# This helps create higher-fidelity mocks.
from windows_use.agent.views import AgentData, AgentStep, Action
from windows_use.agent.registry.views import ToolResult
from windows_use.desktop.views import DesktopState, TreeState


# #############################################################################
# Pytest Fixtures: The foundation of a robust test suite.
# These handle all setup and mocking, keeping tests clean.
# #############################################################################

@pytest.fixture
def mock_prompt_template(mocker):
    """Mocks both PromptTemplate and the 'files' utility it depends on."""
    # Mock the template instance that will be returned by from_file/from_template
    mock_template_instance = mocker.MagicMock()
    mock_template_instance.format.return_value = "formatted prompt"
    
    # Mock the class methods of PromptTemplate
    mocker.patch(
        "windows_use.agent.prompt.service.PromptTemplate.from_file",
        return_value=mock_template_instance
    )
    mocker.patch(
        "windows_use.agent.prompt.service.PromptTemplate.from_template",
        return_value=mock_template_instance
    )
    
    # Mock the file loader utility
    mocker.patch("windows_use.agent.prompt.service.files")
    
    # Return the instance so we can inspect calls to .format()
    return mock_template_instance

@pytest.fixture

def mock_system_info(mocker):
    """Mocks all external system-information gathering functions."""
    mocker.patch("windows_use.agent.prompt.service.pg.size", return_value=(1920, 1080))
    mocker.patch("windows_use.agent.prompt.service.pg.position", return_value=mocker.MagicMock(x=100, y=200))

    # --- THIS IS THE FIX FOR THE DATETIME ERROR ---
    # 1. Patch the entire datetime class where it's imported in your service module.
    mock_datetime_class = mocker.patch("windows_use.agent.prompt.service.datetime")
    
    # 2. Configure the mock. Tell it that when its .now() method is called,
    #    it should return a *real* datetime object so that .strftime() works.
    mock_datetime_class.now.return_value = datetime(2025, 7, 5)

    mocker.patch("windows_use.agent.prompt.service.getuser", return_value="test_user")
    mocker.patch("windows_use.agent.prompt.service.platform.system", return_value="Windows")
    
    mock_home = mocker.MagicMock(spec=Path)
    mock_home.joinpath.return_value.as_posix.return_value = "C:/Users/test_user/Downloads"
    mock_home.as_posix.return_value = "C:/Users/test_user"
    mocker.patch("windows_use.agent.prompt.service.Path.home", return_value=mock_home)

@pytest.fixture
def mock_agent_data(mocker):
    """Provides a consistent, mocked AgentData object."""
    # Create a standard MagicMock for the nested 'action' object
    # This allows us to set .name and .params without autospec restrictions
    mock_action = mocker.MagicMock()
    mock_action.name = "click"
    mock_action.params = {"element_id": 1}

    # Create the main autospecced mock for AgentData
    agent_data = mocker.create_autospec(
        AgentData,
        instance=True,  # Important to mock an instance of the class
        evaluate="This is the evaluation.",
        memory="This is the memory.",
        thought="This is the thought.",
        action=mock_action  # Assign our configured mock_action
    )
    return agent_data

@pytest.fixture
def mock_desktop_state(mocker):
    """Provides a consistent, mocked DesktopState object with autospec."""

    # Step 1: Create a mock for the nested TreeState object.
    mock_tree_state = mocker.create_autospec(TreeState, instance=True)
    mock_tree_state.interactive_elements_to_string.return_value = "Interactive: [Button 'Save']"
    mock_tree_state.informative_elements_to_string.return_value = "Informative: [Text 'Hello World']"
    mock_tree_state.scrollable_elements_to_string.return_value = "Scrollable: [Pane 'Main']"

    # Step 2: Create the main DesktopState mock.
    desktop_state = mocker.create_autospec(DesktopState, instance=True)

    # Step 3: Attach the nested mock as an attribute to the main mock.
    # After fixing the real class, autospec will now allow this.
    desktop_state.tree_state = mock_tree_state

    # Step 4: Configure the methods on the main mock.
    desktop_state.active_app_to_string.return_value = "Active App: Notepad"
    desktop_state.apps_to_string.return_value = "Open Apps: [Notepad, Chrome]"
    
    return desktop_state

# #############################################################################
# Test Class
# #############################################################################

class TestPrompt:
    """Tests the static methods of the Prompt service class."""

    def test_system_prompt(self, mock_prompt_template, mock_system_info):
        """
        Tests `system_prompt` correctly formats all system info.
        """
        # Arrange
        instructions = ["Review the document", "Summarize its contents"]
        
        # Act
        result = Prompt.system_prompt("chrome", "tools_prompt_text", 100, instructions)
        
        # Assert
        expected_format_args = {
            'current_datetime': 'Saturday, July 05, 2025',
            'instructions': 'Review the document\nSummarize its contents',
            'tools_prompt': 'tools_prompt_text',
            'download_directory': 'C:/Users/test_user/Downloads',
            'os': 'Windows',
            'browser': 'chrome',
            'home_dir': 'C:/Users/test_user',
            'user': 'test_user',
            'resolution': '1920x1080',
            'max_steps': 100
        }
        mock_prompt_template.format.assert_called_once_with(**expected_format_args)
        assert result == "formatted prompt"

    def test_action_prompt(self, mock_prompt_template, mock_agent_data):
        """
        Tests `action_prompt` correctly formats agent data.
        """
        # Arrange (handled by fixtures)

        # Act
        result = Prompt.action_prompt(mock_agent_data)

        # Assert
        expected_format_args = {
            'evaluate': "This is the evaluation.",
            'memory': "This is the memory.",
            'thought': "This is the thought.",
            'action_name': "click",
            'action_input': {"element_id": 1}
        }
        mock_prompt_template.format.assert_called_once_with(**expected_format_args)
        assert result == "formatted prompt"

    def test_previous_observation_prompt(self, mock_prompt_template, mocker):
        """
        Tests `previous_observation_prompt` correctly formats the observation string.
        """
        # Arrange
        # We need to mock dedent for this specific test
        mock_dedent = mocker.patch("windows_use.agent.prompt.service.dedent")
        observation_text = "The tool executed successfully."

        # Act
        result = Prompt.previous_observation_prompt(observation_text)

        # Assert
        mock_dedent.assert_called_once()
        # The template is created from the result of dedent, so we assert it was called with ANY string
        mock_prompt_template.format.assert_called_once_with(observation=observation_text)
        assert result == "formatted prompt"

    @pytest.mark.parametrize(
        "tool_result_details, expected_observation",
        [
            pytest.param(
                {'is_success': True, 'content': "Clicked button successfully.", 'error': None}, 
                "Clicked button successfully.", 
                id="Success"
            ),
            pytest.param(
                {'is_success': False, 'content': None, 'error': "Element not found."},
                "Element not found.",
                id="Failure"
            ),
        ]
    )
    def test_observation_prompt_outcomes(self, mock_prompt_template, mock_system_info, mock_desktop_state, mocker, tool_result_details, expected_observation):
        """
        Tests `observation_prompt` for both successful and failed tool executions.
        """
        # Arrange
        agent_step = mocker.create_autospec(AgentStep, step_number=5, max_steps=20)
        tool_result = mocker.create_autospec(ToolResult, **tool_result_details)
        
        # Act
        result = Prompt.observation_prompt("test query", agent_step, tool_result, mock_desktop_state)
        
        # Assert
        expected_format_args = {
            'steps': 5,
            'max_steps': 20,
            'observation': expected_observation,
            'active_app': "Active App: Notepad",
            'cursor_location': '(100,200)',
            'apps': "Open Apps: [Notepad, Chrome]",
            'interactive_elements': "Interactive: [Button 'Save']",
            'informative_elements': "Informative: [Text 'Hello World']",
            'scrollable_elements': "Scrollable: [Pane 'Main']",
            'query': "test query"
        }
        mock_prompt_template.format.assert_called_once_with(**expected_format_args)
        assert result == "formatted prompt"

    def test_observation_prompt_with_no_elements(self, mock_prompt_template, mock_system_info, mock_desktop_state, mocker):
        """
        Tests `observation_prompt` handles cases where no UI elements are found.
        """
        # Arrange
        agent_step = mocker.create_autospec(AgentStep, step_number=5, max_steps=20)
        tool_result = mocker.create_autospec(ToolResult, is_success=True, content="Done.", error=None)
        
        # Override the default mock behavior for this specific test
        mock_desktop_state.tree_state.interactive_elements_to_string.return_value = ""
        mock_desktop_state.tree_state.informative_elements_to_string.return_value = ""
        mock_desktop_state.tree_state.scrollable_elements_to_string.return_value = ""

        # Act
        result = Prompt.observation_prompt("test query", agent_step, tool_result, mock_desktop_state)

        # Assert
        expected_format_args = {
            'steps': 5, 'max_steps': 20, 'observation': "Done.",
            'active_app': "Active App: Notepad", 'cursor_location': '(100,200)',
            'apps': "Open Apps: [Notepad, Chrome]",
            'interactive_elements': 'No interactive elements found', # Verify fallback text
            'informative_elements': 'No informative elements found', # Verify fallback text
            'scrollable_elements': 'No scrollable elements found',  # Verify fallback text
            'query': "test query"
        }
        mock_prompt_template.format.assert_called_once_with(**expected_format_args)
        assert result == "formatted prompt"

    def test_answer_prompt(self, mock_prompt_template, mock_agent_data, mocker):
        """
        Tests `answer_prompt` correctly formats the final answer.
        """
        # Arrange
        tool_result = mocker.create_autospec(ToolResult, content="The final answer is complete.")

        # Act
        result = Prompt.answer_prompt(mock_agent_data, tool_result)

        # Assert
        expected_format_args = {
            'evaluate': "This is the evaluation.",
            'memory': "This is the memory.",
            'thought': "This is the thought.",
            'final_answer': "The final answer is complete."
        }
        mock_prompt_template.format.assert_called_once_with(**expected_format_args)
        assert result == "formatted prompt"