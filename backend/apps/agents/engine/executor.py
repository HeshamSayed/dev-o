"""
Agent Executor

High-level interface for executing agents.
Provides simple API for running agents with tasks.
"""

import logging
from typing import Dict, Any, AsyncGenerator, Optional
from datetime import datetime
from asgiref.sync import sync_to_async

from apps.agents.models import AgentInstance
from apps.tasks.models import Task
from apps.projects.models import Project
from .runtime import AgentRuntime

logger = logging.getLogger(__name__)


class AgentExecutor:
    """
    High-level executor for running agents.

    Provides simplified interface for:
    - Executing agents with tasks
    - Managing agent lifecycle
    - Handling errors and retries
    """

    @staticmethod
    async def execute_agent(
        agent: AgentInstance,
        task: Task,
        stream: bool = True
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Execute an agent with a task.

        Args:
            agent: Agent instance to execute
            task: Task to execute
            stream: Whether to stream events

        Yields:
            Event dictionaries for real-time updates
        """
        try:
            # Load agent type handler
            @sync_to_async
            def get_agent_type_handler():
                return AgentExecutor._get_agent_type_handler(agent)

            agent_type_handler = await get_agent_type_handler()

            # Create runtime
            runtime = AgentRuntime(
                agent=agent,
                agent_type_handler=agent_type_handler
            )

            # Execute task
            async for event in runtime.execute_task(task, stream):
                yield event

        except Exception as e:
            # Get agent name safely in async context
            @sync_to_async
            def get_agent_name():
                return agent.agent_type.name

            agent_name = await get_agent_name()
            logger.exception(f"Error executing agent {agent_name}: {e}")
            yield {
                "type": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            raise

    @staticmethod
    def _get_agent_type_handler(agent: AgentInstance):
        """
        Get agent type handler for an agent.

        Args:
            agent: Agent instance

        Returns:
            Agent type handler instance
        """
        from apps.agents.types.orchestrator import OrchestratorAgent
        from apps.agents.types.architect import ArchitectAgent
        from apps.agents.types.backend_lead import BackendLeadAgent
        from apps.agents.types.frontend_lead import FrontendLeadAgent

        # Map roles to handlers
        handlers = {
            "orchestrator": OrchestratorAgent,
            "architect": ArchitectAgent,
            "backend_lead": BackendLeadAgent,
            "frontend_lead": FrontendLeadAgent,
        }

        handler_class = handlers.get(agent.agent_type.role)

        if not handler_class:
            raise ValueError(f"Unknown agent type: {agent.agent_type.role}")

        return handler_class()

    @staticmethod
    async def execute_project(
        project: Project,
        user_message: str,
        stream: bool = True
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Execute a project from a user message.

        This is the main entry point for user interactions.
        Creates/uses orchestrator agent and starts execution.

        Args:
            project: Project to execute
            user_message: User's message/request
            stream: Whether to stream events

        Yields:
            Event dictionaries
        """
        try:
            # Get or create orchestrator agent
            from apps.agents.models import AgentType, AgentStatus

            @sync_to_async
            def get_or_create_orchestrator():
                orchestrator_type = AgentType.objects.get(role="orchestrator")
                orchestrator = AgentInstance.objects.filter(
                    project=project,
                    agent_type=orchestrator_type
                ).first()

                created = False
                if not orchestrator:
                    orchestrator = AgentInstance.objects.create(
                        project=project,
                        agent_type=orchestrator_type,
                        status=AgentStatus.IDLE
                    )
                    created = True

                return orchestrator, created

            orchestrator, created = await get_or_create_orchestrator()

            if created:
                yield {
                    "type": "agent_created",
                    "agent": "Orchestrator",
                    "timestamp": datetime.now().isoformat()
                }

            # Create task from user message
            @sync_to_async
            def create_task():
                return Task.objects.create(
                    project=project,
                    title=f"User request: {user_message[:100]}",
                    description=user_message,
                    task_type='task',
                    priority=2,  # HIGH priority
                    assigned_to=orchestrator
                )

            task = await create_task()

            yield {
                "type": "task_created",
                "task_id": str(task.id),
                "title": task.title,
                "timestamp": datetime.now().isoformat()
            }

            # Add user message to orchestrator's conversation
            @sync_to_async
            def update_conversation_history():
                orchestrator.conversation_history = orchestrator.conversation_history or []
                orchestrator.conversation_history.append({
                    "role": "user",
                    "content": user_message,
                    "timestamp": datetime.now().isoformat()
                })
                orchestrator.save()

            await update_conversation_history()

            # Execute agent
            async for event in AgentExecutor.execute_agent(orchestrator, task, stream):
                yield event

        except Exception as e:
            logger.exception(f"Error executing project: {e}")
            yield {
                "type": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            raise

    @staticmethod
    def cancel_execution(agent: AgentInstance):
        """
        Cancel an agent's execution.

        Args:
            agent: Agent to cancel
        """
        # This would need to be expanded with actual cancellation logic
        # For now, just log
        logger.info(f"Cancellation requested for agent {agent.agent_type.name}")

        from apps.agents.models import AgentStatus
        agent.status = AgentStatus.IDLE
        agent.status_message = "Cancelled by user"
        agent.save()
