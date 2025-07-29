from _typeshed import Incomplete
from a2a.server.agent_execution import RequestContext as RequestContext
from a2a.server.events.event_queue import EventQueue as EventQueue
from a2a.server.tasks import TaskUpdater as TaskUpdater
from abc import ABC
from gllm_agents.a2a.server.base_executor import BaseA2AExecutor as BaseA2AExecutor
from gllm_agents.agent.base_langchain_agent import BaseLangChainAgent as BaseLangChainAgent
from gllm_agents.utils.logger_manager import LoggerManager as LoggerManager

logger: Incomplete

class BaseLangChainExecutor(BaseA2AExecutor, ABC):
    """Base class for LangChain-based A2A executors.

    This class extends BaseA2AExecutor to provide common functionality for executors
    that work with LangChain-based agents (LangChainAgent and LangGraphAgent).
    It implements shared methods for handling streaming responses and managing
    agent execution, while leaving agent-specific initialization to subclasses.

    Attributes:
        agent (BaseLangChainAgent): The LangChain-based agent instance to be executed.
    """
    agent: BaseLangChainAgent
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Processes an incoming agent request using a LangChain-based agent.

        This method first performs initial checks using _handle_initial_execute_checks.
        If successful, it prepares the _process_stream coroutine and passes it to
        _execute_agent_processing from the base class to manage its lifecycle.
        The _process_stream method is responsible for calling the agent's
        arun_a2a_stream and handling its output.

        Args:
            context (RequestContext): The A2A request context containing message details,
                task ID, and context ID.
            event_queue (EventQueue): The queue for sending A2A events (task status,
                artifacts) back to the server.
        """
