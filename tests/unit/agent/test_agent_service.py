import pytest
from unittest.mock import MagicMock, patch
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import BaseTool
from termcolor import colored
from textwrap import shorten

from windows_use.agent.service import Agent, logger
from windows_use.agent.views import AgentState, AgentStep, AgentResult
from windows_use.agent.registry.views import ToolResult
from windows_use.desktop.service import Desktop
from windows_use.agent.registry.service import Registry
from windows_use.agent.prompt.service import Prompt
from windows_use.agent.utils import extract_agent_data, image_message

# Suppress logging during tests for cleaner output
logger.setLevel(100)

@pytest.fixture
def mock_desktop():
    """Mocks the Desktop class."""
    mock = MagicMock(spec=Desktop)
    mock.get_state.return_value = MagicMock(screenshot="mock_screenshot_data")
    return mock

@pytest.fixture
def mock_registry():
    """Mocks the Registry class."""
    mock = MagicMock(spec=Registry)
    mock.get_tools_prompt.return_value = "Mock Tools Prompt"
    mock.execute.return_value = ToolResult(is_success=True, content="Tool executed")
    mock.tools = []
    return mock

@pytest.fixture
def mock_llm():
    """Mocks the BaseChatModel (LLM)."""
    mock = MagicMock(spec=BaseChatModel)
    mock.invoke.return_value = AIMessage(
        content="<thought>Mock thought</thought><action_name>Done Tool</action_name><action_input>{\"answer\": \"Task done\"}</action_input>"
    )
    return mock

@pytest.fixture
def mock_agent_state():
    """Mocks the AgentState class."""
    mock = MagicMock(spec=AgentState)
    mock.messages = []
    mock.consecutive_failures = 0
    mock.is_done.return_value = False
    mock.previous_observation = None
    mock.query = "test query"
    mock.result = None
    mock.error = None
    mock.agent_data = MagicMock(
        thought="Mock thought",
        action=MagicMock(name="MockTool", params={"param": "value"}),
    )
    return mock

@pytest.fixture
def mock_agent_step():
    """Mocks the AgentStep class."""
    mock = MagicMock(spec=AgentStep)
    mock.step_number = 0
    mock.max_steps = 100
    mock.is_last_step.return_value = False
    return mock

@pytest.fixture
def agent_instance(
    mock_desktop,
    mock_registry,
    mock_llm,
    mock_agent_state,
    mock_agent_step,
):
    """Provides an Agent instance with mocked dependencies."""
    # Use patch to replace classes with mocks during Agent initialization
    with patch("windows_use.agent.service.Desktop", return_value=mock_desktop), \
         patch("windows_use.agent.service.Registry", return_value=mock_registry), \
         patch("windows_use.agent.service.AgentState", return_value=mock_agent_state), \
         patch("windows_use.agent.service.AgentStep", return_value=mock_agent_step):
        agent = Agent(llm=mock_llm)
        # Manually re-assign the mock instances to the agent for direct control in tests
        agent.desktop = mock_desktop
        agent.registry = mock_registry
        agent.llm = mock_llm
        agent.agent_state = mock_agent_state
        agent.agent_step = mock_agent_step
        return agent

class TestAgent:
    """Tests for the Agent class in windows_use.agent.service."""

    def test_init_default_values(self):
        """Test that the Agent initializes with default values correctly."""
        with patch('windows_use.agent.service.Registry') as mock_reg:
            agent = Agent(llm=MagicMock(spec=BaseChatModel))
            assert agent.name == "Windows Use"
            assert agent.description == "An agent that can interact with GUI elements on Windows"
            assert agent.instructions == []
            assert agent.browser == "edge"
            assert agent.consecutive_failures == 3
            assert agent.agent_step.max_steps == 100
            assert agent.use_vision is False
            assert isinstance(agent.registry, MagicMock)
            assert isinstance(agent.desktop, Desktop)
            assert isinstance(agent.agent_state, AgentState)
            assert isinstance(agent.agent_step, AgentStep)
            assert agent.llm is not None

    def test_init_custom_values(self):
        """Test that the Agent initializes with custom values correctly."""
        mock_tool = MagicMock(spec=BaseTool)
        mock_tool.name = "CustomMockTool"
        mock_tool.description = "A mock tool for testing purposes."
        mock_tool.args = {}

        # We must patch the Registry here because its __init__ accesses tool attributes
        with patch('windows_use.agent.service.Registry') as mock_reg_class:
            mock_registry_instance = MagicMock()
            mock_registry_instance.tools = [mock_tool] # Simulate the tools list
            mock_reg_class.return_value = mock_registry_instance

            agent = Agent(
                instructions=["custom instruction"],
                additional_tools=[mock_tool],
                browser="chrome",
                llm=MagicMock(spec=BaseChatModel),
                consecutive_failures=5,
                max_steps=50,
                use_vision=True,
            )
            assert agent.instructions == ["custom instruction"]
            assert agent.browser == "chrome"
            assert agent.consecutive_failures == 5
            assert agent.agent_step.max_steps == 50
            assert agent.use_vision is True
            assert mock_tool in agent.registry.tools

    @patch("windows_use.agent.service.extract_agent_data")
    @patch("windows_use.agent.service.logger")
    def test_reason(self, mock_logger, mock_extract_agent_data, agent_instance):
        """Test the reason method's logic."""
        mock_message = AIMessage(content="mock message")
        agent_instance.llm.invoke.return_value = mock_message
        mock_agent_data = MagicMock(thought="Test Thought")
        mock_extract_agent_data.return_value = mock_agent_data

        agent_instance.reason()

        agent_instance.llm.invoke.assert_called_once_with(agent_instance.agent_state.messages)
        mock_extract_agent_data.assert_called_once_with(message=mock_message)
        agent_instance.agent_state.update_state.assert_called_once_with(
            agent_data=mock_agent_data, messages=[mock_message]
        )

    @patch("windows_use.agent.service.Prompt")
    @patch("windows_use.agent.service.image_message")
    @pytest.mark.parametrize("use_vision_flag", [True, False])
    def test_action_success(self, mock_image_message, mock_prompt, use_vision_flag, agent_instance):
        """Test the action method for success cases."""
        agent_instance.use_vision = use_vision_flag
        agent_instance.agent_state.messages = [HumanMessage(content="prior"), AIMessage(content="pop")]
        agent_instance.agent_state.agent_data.action.name = "TestTool"
        agent_instance.agent_state.agent_data.action.params = {"arg1": "val1"}
        agent_instance.registry.execute.return_value = ToolResult(is_success=True, content="Tool success")
        mock_prompt.action_prompt.return_value = "action_prompt"
        mock_prompt.observation_prompt.return_value = "obs_prompt"
        mock_image_message.return_value = HumanMessage(content="image_message")

        agent_instance.action()

        agent_instance.registry.execute.assert_called_once_with(
            tool_name="TestTool", desktop=agent_instance.desktop, arg1="val1"
        )
        final_message = HumanMessage(content="image_message") if use_vision_flag else HumanMessage(content="obs_prompt")
        agent_instance.agent_state.update_state.assert_called_once_with(
            agent_data=None, observation="Tool success", messages=[AIMessage(content="action_prompt"), final_message]
        )

    @patch("windows_use.agent.service.Prompt")
    @patch("windows_use.agent.service.image_message")
    def test_action_failure(self, mock_image_message, mock_prompt, agent_instance):
        """Test the action method for failure cases."""
        agent_instance.use_vision = False
        agent_instance.agent_state.messages = [HumanMessage(content="prior"), AIMessage(content="pop")]
        agent_instance.registry.execute.return_value = ToolResult(is_success=False, error="Tool failed")
        mock_prompt.action_prompt.return_value = "action_prompt"
        mock_prompt.observation_prompt.return_value = "obs_prompt"

        agent_instance.action()

        agent_instance.agent_state.update_state.assert_called_once_with(
            agent_data=None, observation="Tool failed", messages=[AIMessage(content="action_prompt"), HumanMessage(content="obs_prompt")]
        )
        mock_image_message.assert_not_called()

    @patch("windows_use.agent.service.Prompt")
    def test_answer(self, mock_prompt, agent_instance):
        """Test the answer method's logic."""
        agent_instance.agent_state.messages = [HumanMessage(content="prior"), AIMessage(content="pop")]
        agent_instance.agent_state.agent_data.action.name = "Done Tool"
        agent_instance.agent_state.agent_data.action.params = {"answer": "Final Answer"}
        agent_instance.registry.execute.return_value = ToolResult(is_success=True, content="Final Content")
        mock_prompt.answer_prompt.return_value = "answer_prompt"

        agent_instance.answer()

        agent_instance.registry.execute.assert_called_once_with(tool_name="Done Tool", desktop=None, answer="Final Answer")
        agent_instance.agent_state.update_state.assert_called_once_with(
            agent_data=None, observation=None, result="Final Content", messages=[AIMessage(content="answer_prompt")]
        )

    @patch("windows_use.agent.service.Prompt")
    def test_invoke_max_steps_reached(self, mock_prompt, agent_instance):
        """Test invoke method when maximum steps are reached."""
        agent_instance.agent_step.is_last_step.return_value = True

        result = agent_instance.invoke("test query")
        
        assert result.is_done is False
        assert result.error == "Maximum steps reached."

    @patch("windows_use.agent.service.Prompt")
    def test_invoke_consecutive_failures_exceeded(self, mock_prompt, agent_instance):
        """Test invoke method when consecutive failures are exceeded."""
        # Setup to fail
        agent_instance.consecutive_failures = 1 # Agent fails after 1 try
        agent_instance.agent_state.consecutive_failures = 1 # It has already failed once
        agent_instance.agent_state.error = "Mock Error"

        result = agent_instance.invoke("test query")

        assert result.is_done is False
        assert result.error == "Mock Error"

    @patch("windows_use.agent.service.Prompt")
    def test_invoke_reason_exception_handling(self, mock_prompt, agent_instance):
        """Test exception handling for the reason method."""
        agent_instance.consecutive_failures = 2 # Allow for 1 failure
        # Mock reason to fail once, then succeed
        agent_instance.reason = MagicMock(side_effect=[Exception("Reason Error 1"), None])
        # Mock other parts to let the loop run
        agent_instance.action = MagicMock()
        agent_instance.agent_step.is_last_step.side_effect = [False, False, True] # Run loop twice
        agent_instance.agent_state.is_done.return_value = False

        agent_instance.invoke("test query")

        assert agent_instance.reason.call_count == 2
        assert agent_instance.agent_state.consecutive_failures == 1
        assert agent_instance.agent_state.error == "Reason Error 1"
        agent_instance.action.assert_called_once() # Should be called after success

    @patch("windows_use.agent.service.Prompt")
    def test_invoke_task_done(self, mock_prompt, agent_instance):
        """Test invoke method when the task is completed."""
        agent_instance.reason = MagicMock() # Mock reason to prevent its logic
        agent_instance.agent_state.is_done.return_value = True # Make it "done"
        agent_instance.answer = MagicMock()
        agent_instance.agent_state.result = "Final Result"

        result = agent_instance.invoke("test query")

        agent_instance.reason.assert_called_once()
        agent_instance.answer.assert_called_once()
        assert result.is_done is True
        assert result.content == "Final Result"

    @patch("windows_use.agent.service.Prompt")
    def test_invoke_action_path(self, mock_prompt, agent_instance):
        """Test invoke method's normal action path."""
        agent_instance.reason = MagicMock() # Mock reason to prevent its logic
        agent_instance.agent_state.is_done.return_value = False # Not done
        agent_instance.action = MagicMock()
        agent_instance.agent_step.is_last_step.side_effect = [False, True] # Run loop once

        result = agent_instance.invoke("test query")

        agent_instance.reason.assert_called_once()
        agent_instance.action.assert_called_once()
        agent_instance.agent_step.increment_step.assert_called_once()
        assert result.is_done is False

    @patch("windows_use.agent.service.Prompt")
    def test_invoke_general_exception_handling(self, mock_prompt, agent_instance):
        """Test invoke method's general exception handling."""
        agent_instance.registry.get_tools_prompt.side_effect = Exception("General Invoke Error")

        result = agent_instance.invoke("test query")
        
        assert result.is_done is False
        assert result.error == "General Invoke Error"

    @patch("windows_use.agent.service.Console")
    def test_print_response(self, mock_console, agent_instance):
        """Test print_response method."""
        agent_instance.invoke = MagicMock(return_value=AgentResult(content="Mock Content", is_done=True))
        mock_console_instance = mock_console.return_value

        agent_instance.print_response("test query")

        agent_instance.invoke.assert_called_once_with("test query")
        mock_console_instance.print.assert_called_once()

    @patch("windows_use.agent.service.Console")
    def test_print_response_with_error(self, mock_console, agent_instance):
        """Test print_response method when invoke returns an error."""
        agent_instance.invoke = MagicMock(return_value=AgentResult(error="Mock Error"))
        mock_console_instance = mock_console.return_value
        
        agent_instance.print_response("test query")
        
        agent_instance.invoke.assert_called_once_with("test query")
        mock_console_instance.print.assert_called_once()
