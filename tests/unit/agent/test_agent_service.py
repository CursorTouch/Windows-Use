# tests/unit/agent/test_agent_service.py

import pytest
from unittest.mock import MagicMock, patch
import json
from windows_use.agent.service import Agent
from windows_use.agent.views import AgentResult
from windows_use.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

class TestAgent:
    """
    Tests for the Agent class in windows_use.agent.service.
    """

    @pytest.fixture
    def mock_llm(self):
        """Mock LLM."""
        mock = MagicMock()
        mock.model_name = "test-model"
        mock.provider = "test-provider"
        return mock

    @pytest.fixture
    def mock_desktop(self):
        """Mock Desktop."""
        with patch("windows_use.agent.service.Desktop") as mock_class:
            mock_instance = mock_class.return_value
            mock_instance.get_state.return_value = MagicMock()
            mock_instance.get_default_language.return_value = "English"
            # mock_instance.auto_minimize is a context manager
            mock_instance.auto_minimize.return_value.__enter__.return_value = None
            yield mock_instance

    @pytest.fixture
    def mock_prompt(self):
        """Mock Prompt with string return values for Pydantic."""
        with patch("windows_use.agent.service.Prompt") as mock_p:
            mock_p.system_prompt.return_value = "System prompt"
            mock_p.observation_prompt.return_value = "Observation prompt"
            mock_p.previous_observation_prompt.return_value = "Prev observation prompt"
            mock_p.action_prompt.return_value = "Action prompt"
            mock_p.answer_prompt.return_value = "Answer prompt"
            yield mock_p

    @pytest.fixture
    def mock_console(self):
        """Mock Console."""
        with patch("windows_use.agent.service.Console") as mock_class:
            yield mock_class.return_value

    def test_init(self, mock_llm, mock_desktop, mock_console):
        """Test Agent initialization."""
        agent = Agent(llm=mock_llm, instructions=["Test instruction"])
        assert agent.instructions == ["Test instruction"]
        assert agent.state.max_steps == 25
        assert agent.state.max_consecutive_failures == 3

    @patch("windows_use.agent.service.Registry")
    @patch("windows_use.agent.service.WatchDog")
    def test_invoke_done(self, mock_watchdog, mock_registry_class, mock_llm, mock_desktop, mock_prompt, mock_console):
        """Test invoke method when task is completed via done_tool."""
        mock_registry = mock_registry_class.return_value
        
        # When execute is called, it returns a ToolResult-like object
        mock_response = MagicMock()
        mock_response.content = "Job's done"
        mock_response.is_success = True
        mock_registry.execute.return_value = mock_response
        
        # Mock LLM response - agent expects ToolMessage for tool calls
        mock_llm.invoke.return_value = ToolMessage(
            id="call_1",
            name="done_tool",
            params={"answer": "Job's done", "thought": "I have finished the task."},
        )
        
        agent = Agent(llm=mock_llm)
        result = agent.invoke("test query")
        
        assert isinstance(result, AgentResult)
        assert result.is_done is True
        assert result.content == "Job's done"
        assert mock_llm.invoke.call_count == 1

    @patch("windows_use.agent.service.Registry")
    @patch("windows_use.agent.service.WatchDog")
    def test_invoke_max_steps(self, mock_watchdog, mock_registry_class, mock_llm, mock_desktop, mock_prompt, mock_console):
        """Test invoke method stops after max_steps."""
        mock_registry = mock_registry_class.return_value
        mock_response = MagicMock()
        mock_response.content = "Step result"
        mock_response.is_success = True
        mock_registry.execute.return_value = mock_response
        
        # Mock LLM response (non-done action)
        mock_llm.invoke.return_value = ToolMessage(
            id="call_1",
            name="click_tool",
            params={"loc": [10, 10], "thought": "Keep working"},
        )
        
        agent = Agent(llm=mock_llm, max_steps=2)
        result = agent.invoke("test query")
        
        assert result.is_done is False
        assert "Max steps reached" in result.error
        assert mock_llm.invoke.call_count == 2

    def test_print_response(self, mock_llm, mock_desktop, mock_console):
        """Test print_response utility."""
        agent = Agent(llm=mock_llm)
        
        # Mock invoke to return a success result
        with patch.object(Agent, 'invoke') as mock_invoke:
            mock_invoke.return_value = AgentResult(is_done=True, content="Success")
            agent.print_response("test query")
            
        # Verify it called console.print with Markdown
        from rich.markdown import Markdown
        assert mock_console.print.called
        args = mock_console.print.call_args[0]
        assert isinstance(args[0], Markdown)

    def test_print_response_error(self, mock_llm, mock_desktop, mock_console):
        """Test print_response with error."""
        agent = Agent(llm=mock_llm)
        
        # Mock invoke to return an error result
        with patch.object(Agent, 'invoke') as mock_invoke:
            mock_invoke.return_value = AgentResult(is_done=False, error="Some error")
            agent.print_response("test query")
            
        from rich.markdown import Markdown
        assert mock_console.print.called
        args = mock_console.print.call_args[0]
        assert isinstance(args[0], Markdown)
