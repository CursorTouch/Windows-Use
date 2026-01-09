# tests/unit/agent/test_agent_views.py

import pytest
from unittest.mock import MagicMock
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from windows_use.agent.views import AgentState, AgentStep, AgentResult, Action, AgentData
from windows_use.tree.views import TreeState, TreeElementNode, TextElementNode, ScrollElementNode, BoundingBox, Center

class TestAgentViews:
    """
    Tests for the data models and view-related classes in windows_use.agent.views.
    """

    def test_agent_state_initialization(self):
        """
        Test AgentState initialization with default and provided values.
        """
        state = AgentState()
        assert isinstance(state.id, str)
        assert state.consecutive_failures == 0
        # --- FIX: The default value is now None, not an empty string ---
        assert state.result is None
        assert state.error is None
        assert state.agent_data is None
        assert state.messages == []
        assert state.previous_observation is None
        assert state.query is None

    @pytest.mark.parametrize(
        "agent_data_action_name, expected_is_done",
        [
            (None, False),
            ("Some Tool", False),
            ("Done Tool", True),
        ],
    )
    def test_agent_state_is_done(self, agent_data_action_name, expected_is_done):
        """
        Test `AgentState.is_done` method with various `agent_data.action.name` values.
        """
        state = AgentState()
        if agent_data_action_name is not None:
            # Create a mock with the nested structure
            mock_action = MagicMock(spec=Action)
            mock_action.name = agent_data_action_name
            state.agent_data = MagicMock(spec=AgentData)
            state.agent_data.action = mock_action
        else:
            state.agent_data = None

        assert state.is_done() == expected_is_done

    def test_agent_state_init_state(self):
        """
        Test `AgentState.init_state` method correctly initializes state for a new query.
        """
        state = AgentState(
            query="old query",
            consecutive_failures=5,
            result="old result",
            messages=[HumanMessage(content="old message")],
        )
        new_messages = [SystemMessage(content="new system"), HumanMessage(content="new human")]
        state.init_state(query="new query", messages=new_messages)

        assert state.query == "new query"
        assert state.consecutive_failures == 0
        assert state.result is None
        assert state.messages == new_messages

    def test_agent_state_update_state(self):
        """
        Test `AgentState.update_state` correctly updates various state attributes.
        """
        initial_messages = [HumanMessage(content="initial")]
        state = AgentState(messages=initial_messages)
        mock_agent_data = MagicMock(spec=AgentData)
        new_messages = [AIMessage(content="new ai message")]
        
        state.update_state(
            agent_data=mock_agent_data,
            observation="new observation",
            result="new result",
            messages=new_messages,
        )

        assert state.result == "new result"
        assert state.previous_observation == "new observation"
        assert state.agent_data == mock_agent_data
        assert state.messages == initial_messages + new_messages

    def test_agent_step_initialization(self):
        """
        Test AgentStep initialization.
        """
        step = AgentStep(max_steps=10)
        assert step.step_number == 0
        assert step.max_steps == 10

    @pytest.mark.parametrize(
        "step_number, max_steps, expected_is_last_step",
        [
            (0, 1, True),
            (0, 10, False),
            (9, 10, True),
            (10, 10, True),
            (5, 5, True),
        ],
    )
    def test_agent_step_is_last_step(self, step_number, max_steps, expected_is_last_step):
        """
        Test `AgentStep.is_last_step` method logic.
        """
        step = AgentStep(step_number=step_number, max_steps=max_steps)
        assert step.is_last_step() == expected_is_last_step

    def test_agent_step_increment_step(self):
        """
        Test `AgentStep.increment_step` method.
        """
        step = AgentStep(max_steps=10)
        assert step.step_number == 0
        step.increment_step()
        assert step.step_number == 1
        step.increment_step()
        assert step.step_number == 2

    def test_agent_result_initialization(self):
        """
        Test AgentResult initialization with default and provided values.
        """
        result = AgentResult()
        assert result.is_done is False
        assert result.content is None
        assert result.error is None

        result_custom = AgentResult(is_done=True, content="Success", error="No error")
        assert result_custom.is_done is True
        assert result_custom.content == "Success"
        assert result_custom.error == "No error"

    def test_action_initialization(self):
        """
        Test Action initialization.
        """
        action = Action(name="test_action", params={"key": "value"})
        assert action.name == "test_action"
        assert action.params == {"key": "value"}

    def test_agent_data_initialization(self):
        """
        Test AgentData initialization with default and provided values.
        """
        agent_data = AgentData()
        assert agent_data.evaluate is None
        assert agent_data.memory is None
        assert agent_data.thought is None
        assert agent_data.action is None

        mock_action = Action(name="mock_action", params={})
        agent_data_custom = AgentData(
            evaluate="eval", memory="mem", thought="thought", action=mock_action
        )
        assert agent_data_custom.evaluate == "eval"
        assert agent_data_custom.memory == "mem"
        assert agent_data_custom.thought == "thought"
        assert agent_data_custom.action == mock_action
