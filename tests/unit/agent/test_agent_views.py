# tests/unit/agent/test_agent_views.py

import pytest
from windows_use.agent.views import AgentResult

class TestAgentViews:
    """
    Tests for the data models in windows_use.agent.views.
    """

    def test_agent_result_initialization(self):
        """
        Test AgentResult initialization.
        """
        result = AgentResult(is_done=False)
        assert result.is_done is False
        assert result.content is None
        assert result.error is None

        result_custom = AgentResult(is_done=True, content="Success", error="No error")
        assert result_custom.is_done is True
        assert result_custom.content == "Success"
        assert result_custom.error == "No error"
