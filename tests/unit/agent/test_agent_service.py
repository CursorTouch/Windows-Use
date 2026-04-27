# tests/unit/agent/test_agent_service.py

import pytest
from unittest.mock import MagicMock, patch
import json
from windows_use.agent.service import Agent
from windows_use.agent.views import AgentResult
from windows_use.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from windows_use.providers.events import LLMEvent, LLMEventType, ToolCall
from windows_use.providers.views import TokenUsage

class TestAgent:
    """
    Tests for the Agent class in windows_use.agent.service.
    """

    @pytest.fixture
    def mock_llm(self):
        mock = MagicMock()
        mock.model_name = "test-model"
        mock.provider = "test-provider"
        mock.get_metadata.return_value.context_window = 100000
        return mock

    @pytest.fixture
    def mock_desktop(self):
        with patch("windows_use.agent.service.Desktop") as mock_class:
            mock_instance = mock_class.return_value
            mock_instance.get_state.return_value = MagicMock()
            mock_instance.get_default_language.return_value = "English"
            mock_instance.use_vision = False
            mock_instance.use_accessibility = True
            mock_instance.desktop_state.active_window_to_string.return_value = "Active: Notepad"
            mock_instance.desktop_state.windows_to_string.return_value = "Windows: [Notepad]"
            mock_instance.desktop_state.tree_state.interactive_elements_to_string.return_value = "elements"
            mock_instance.desktop_state.tree_state.scrollable_elements_to_string.return_value = "scrollable"
            mock_instance.desktop_state.active_desktop_to_string.return_value = "Desktop 1"
            mock_instance.desktop_state.desktops_to_string.return_value = "Desktops: [1]"
            mock_instance.desktop_state.active_window.handle = 12345
            mock_instance.auto_minimize.return_value.__enter__.return_value = None
            yield mock_instance

    @pytest.fixture
    def mock_console(self):
        with patch("windows_use.agent.service.Console") as mock_class:
            yield mock_class.return_value

    def test_init(self, mock_llm, mock_desktop, mock_console):
        agent = Agent(llm=mock_llm, instructions=["Test instruction"])
        assert agent.instructions == ["Test instruction"]
        assert agent.state.max_steps == 25
        assert agent.state.max_consecutive_failures == 3

    @patch("windows_use.agent.service.Registry")
    @patch("windows_use.agent.service.WatchDog")
    def test_invoke_done(self, mock_watchdog, mock_registry_class, mock_llm, mock_desktop, mock_console):
        mock_registry = mock_registry_class.return_value

        mock_response = MagicMock()
        mock_response.content = "Job's done"
        mock_response.is_success = True
        mock_registry.execute.return_value = mock_response

        mock_llm.invoke.return_value = LLMEvent(
            type=LLMEventType.TOOL_CALL,
            tool_call=ToolCall(id="call_1", name="done_tool", params={"answer": "Job's done", "thought": "I have finished the task."}),
            usage=TokenUsage(),
        )

        agent = Agent(llm=mock_llm)
        result = agent.invoke("test query")

        assert isinstance(result, AgentResult)
        assert result.is_done is True
        assert result.content == "Job's done"
        assert mock_llm.invoke.call_count == 1

    @patch("windows_use.agent.service.Registry")
    @patch("windows_use.agent.service.WatchDog")
    def test_invoke_max_steps(self, mock_watchdog, mock_registry_class, mock_llm, mock_desktop, mock_console):
        mock_registry = mock_registry_class.return_value
        mock_response = MagicMock()
        mock_response.content = "Step result"
        mock_response.is_success = True
        mock_registry.execute.return_value = mock_response

        mock_llm.invoke.return_value = LLMEvent(
            type=LLMEventType.TOOL_CALL,
            tool_call=ToolCall(id="call_1", name="click_tool", params={"loc": [10, 10], "thought": "Keep working"}),
            usage=TokenUsage(),
        )

        agent = Agent(llm=mock_llm, max_steps=2)
        result = agent.invoke("test query")

        assert result.is_done is False
        assert "maximum number of steps" in result.error
        assert mock_llm.invoke.call_count == 2
