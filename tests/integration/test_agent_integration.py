"""Integration tests for the Windows-Use agent."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from windows_use.agent.service import Agent
from windows_use.agent.views import AgentResult
from windows_use.llms.base import BaseChatLLM
from windows_use.llms.views import ChatLLMResponse
from windows_use.messages import AIMessage
from windows_use.exceptions import ValidationError, LLMError, TimeoutError


class MockLLM:
    """Mock LLM for testing."""
    
    def __init__(self, responses=None):
        self.responses = responses or []
        self.call_count = 0
        
    @property
    def model_name(self) -> str:
        return "mock-model"
    
    @property
    def provider(self) -> str:
        return "mock-provider"
    
    def invoke(self, messages, structured_output=None):
        if self.call_count >= len(self.responses):
            raise Exception("No more mock responses available")
        
        response = self.responses[self.call_count]
        self.call_count += 1
        
        if isinstance(response, Exception):
            raise response
        
        return ChatLLMResponse(
            message=AIMessage(content=response),
            usage=None
        )


@pytest.fixture
def mock_desktop():
    """Mock desktop service."""
    with patch('windows_use.agent.service.Desktop') as mock:
        desktop_instance = Mock()
        desktop_instance.get_state.return_value = Mock(
            apps=[],
            active_app=None,
            screenshot=None,
            tree_state=Mock(interactive_nodes=[])
        )
        mock.return_value = desktop_instance
        yield desktop_instance


@pytest.fixture
def mock_registry():
    """Mock tool registry."""
    with patch('windows_use.agent.service.Registry') as mock:
        registry_instance = Mock()
        registry_instance.execute.return_value = Mock(
            is_success=True,
            content="Tool executed successfully",
            error=None
        )
        mock.return_value = registry_instance
        yield registry_instance


class TestAgentIntegration:
    """Integration tests for the Agent class."""
    
    def test_agent_initialization(self, mock_desktop, mock_registry):
        """Test agent initialization with default parameters."""
        agent = Agent()
        
        assert agent.name == 'Windows Use'
        assert agent.max_steps == 25
        assert agent.max_consecutive_failures == 3
        assert not agent.use_vision
        assert not agent.auto_minimize
        assert agent.instructions == []
    
    def test_agent_initialization_with_custom_params(self, mock_desktop, mock_registry):
        """Test agent initialization with custom parameters."""
        instructions = ["Custom instruction 1", "Custom instruction 2"]
        mock_llm = MockLLM()
        
        agent = Agent(
            instructions=instructions,
            llm=mock_llm,
            max_steps=10,
            max_consecutive_failures=5,
            use_vision=True,
            auto_minimize=True
        )
        
        assert agent.instructions == instructions
        assert agent.llm == mock_llm
        assert agent.max_steps == 10
        assert agent.max_consecutive_failures == 5
        assert agent.use_vision
        assert agent.auto_minimize
    
    def test_empty_query_validation(self, mock_desktop, mock_registry):
        """Test that empty queries raise ValidationError."""
        agent = Agent()
        
        with pytest.raises(ValidationError) as exc_info:
            agent.invoke("")
        
        assert "Query cannot be empty" in str(exc_info.value)
        assert exc_info.value.field == "query"
    
    def test_whitespace_only_query_validation(self, mock_desktop, mock_registry):
        """Test that whitespace-only queries raise ValidationError."""
        agent = Agent()
        
        with pytest.raises(ValidationError) as exc_info:
            agent.invoke("   \n\t  ")
        
        assert "Query cannot be empty" in str(exc_info.value)


@pytest.mark.integration
class TestAgentWithRealComponents:
    """Integration tests using more realistic components."""
    
    @pytest.mark.slow
    def test_agent_desktop_interaction(self):
        """Test agent interaction with desktop components."""
        # This test would require a real desktop environment
        # Skip in CI/CD environments
        pytest.skip("Requires interactive desktop environment")
    
    @pytest.mark.slow
    def test_agent_memory_persistence(self):
        """Test agent memory persistence across sessions."""
        # This test would verify memory tool functionality
        pytest.skip("Requires file system access and persistence")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])