from abc import ABC, abstractmethod

from windows_use.agent.views import AgentResult


class BaseAgent(ABC):
    """
    Abstract Base Class for all Agents.
    """

    @abstractmethod
    def invoke(self, query: str) -> AgentResult:
        """
        Executes a task/query and returns a result.
        """
        pass

    @abstractmethod
    async def ainvoke(self, query: str) -> AgentResult:
        """
        Asynchronously executes a task/query and returns a result.
        """
        pass
