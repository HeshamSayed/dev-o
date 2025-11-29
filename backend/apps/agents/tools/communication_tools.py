"""
Communication Tools

Tools for inter-agent communication and user interaction.
Enable agents to collaborate and request input.
"""

import logging
from typing import Dict, Any
from datetime import datetime
from channels.db import database_sync_to_async

from .base import BaseTool, ToolResult
from apps.agents.models import AgentInstance, AgentMessage, AgentStatus
from apps.context.services.event_store import EventStore

logger = logging.getLogger(__name__)


class SendMessageTool(BaseTool):
    """Send a message to another agent."""

    @property
    def name(self) -> str:
        return "send_message"

    @property
    def description(self) -> str:
        return "Send a message to another agent for coordination or requesting information."

    @property
    def parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "recipient_agent_id": {
                    "type": "string",
                    "description": "ID of the agent to send message to"
                },
                "message": {
                    "type": "string",
                    "description": "Message content"
                },
                "message_type": {
                    "type": "string",
                    "description": "Type of message: info, question, request, update",
                    "enum": ["info", "question", "request", "update"]
                },
                "requires_response": {
                    "type": "boolean",
                    "description": "Whether this message requires a response"
                }
            },
            "required": ["recipient_agent_id", "message", "message_type"]
        }

    async def execute(
        self,
        arguments: Dict[str, Any],
        context: Dict[str, Any]
    ) -> ToolResult:
        """Send message to another agent."""
        is_valid, error = self.validate_arguments(arguments)
        if not is_valid:
            return ToolResult(
                success=False,
                message=f"Invalid arguments: {error}",
                error_code="INVALID_ARGS"
            )

        recipient_id = arguments["recipient_agent_id"]
        message_content = arguments["message"]
        message_type = arguments["message_type"]
        requires_response = arguments.get("requires_response", False)

        project = context["project"]
        sender = context["agent"]

        try:
            # Get recipient agent and send message
            @database_sync_to_async
            def send_message_to_agent():
                # Get recipient agent
                try:
                    recipient = AgentInstance.objects.filter(
                        id=recipient_id,
                        project=project
                    ).first()
                except Exception as e:
                    # Handle invalid UUID or other validation errors
                    return None, f"Invalid agent ID format: {str(e)}"

                if not recipient:
                    return None, f"Agent not found with ID: {recipient_id}. Use hire_agent first to create agents."

                # Create message
                message = AgentMessage.objects.create(
                    project=project,
                    from_agent=sender,
                    to_agent=recipient,
                    message_type=message_type,
                    content=message_content,
                    requires_response=requires_response
                )

                # Add to recipient's conversation history
                recipient_history = recipient.conversation_history or []
                recipient_history.append({
                    "role": "agent",
                    "from": sender.agent_type.name,
                    "message": message_content,
                    "timestamp": datetime.now().isoformat()
                })
                recipient.conversation_history = recipient_history
                recipient.save(update_fields=['conversation_history'])

                return (message, recipient, sender.agent_type.name, recipient.agent_type.name), None

            result, error = await send_message_to_agent()

            if error:
                return ToolResult(
                    success=False,
                    message=error,
                    error_code="AGENT_NOT_FOUND"
                )

            message, recipient, sender_name, recipient_name = result

            # Log event
            @database_sync_to_async
            def log_message_event():
                EventStore.log_event(
                    project=project,
                    event_type='message_sent',
                    event_data={
                        "from": str(sender.id),
                        "to": str(recipient.id),
                        "type": message_type,
                        "requires_response": requires_response
                    },
                    actor_type='agent',
                    actor_id=str(sender.id)
                )

            await log_message_event()

            logger.info(f"Message sent: {sender_name} → {recipient_name}")

            return ToolResult(
                success=True,
                message=f"Message sent to {recipient_name}",
                data={
                    "message_id": str(message.id),
                    "recipient": recipient_name,
                    "requires_response": requires_response
                }
            )

        except Exception as e:
            logger.exception(f"Error sending message: {e}")
            return ToolResult(
                success=False,
                message=f"Error sending message: {str(e)}",
                error_code="SEND_ERROR"
            )


class AskUserTool(BaseTool):
    """Ask the user for input."""

    @property
    def name(self) -> str:
        return "ask_user"

    @property
    def description(self) -> str:
        return "Ask the user a question when you need clarification or input to proceed."

    @property
    def parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "Question to ask the user"
                },
                "context": {
                    "type": "string",
                    "description": "Context for why you're asking this question"
                },
                "options": {
                    "type": "array",
                    "description": "Optional list of suggested answers",
                    "items": {"type": "string"}
                }
            },
            "required": ["question"]
        }

    async def execute(
        self,
        arguments: Dict[str, Any],
        context: Dict[str, Any]
    ) -> ToolResult:
        """Ask user for input."""
        is_valid, error = self.validate_arguments(arguments)
        if not is_valid:
            return ToolResult(
                success=False,
                message=f"Invalid arguments: {error}",
                error_code="INVALID_ARGS"
            )

        question = arguments["question"]
        question_context = arguments.get("context", "")
        options = arguments.get("options", [])

        project = context["project"]
        agent = context["agent"]

        try:
            # Create user message
            @database_sync_to_async
            def create_message():
                return AgentMessage.objects.create(
                    project=project,
                    from_agent=agent,
                    to_agent=None,  # None means to user
                    message_type='question',
                    content={
                        "question": question,
                        "context": question_context,
                        "options": options
                    },
                    requires_response=True
                )

            message = await create_message()

            # Update agent status to waiting for input
            @database_sync_to_async
            def update_agent_status():
                agent.status = AgentStatus.WAITING_INPUT
                agent.status_message = f"Waiting for user response: {question[:100]}"
                agent.save()

            await update_agent_status()

            # Log event
            @database_sync_to_async
            def log_user_input_event():
                EventStore.log_event(
                    project=project,
                    event_type='user_input_requested',
                    event_data={
                        "agent": str(agent.id),
                        "question": question,
                        "options": options
                    },
                    actor_type='agent',
                    actor_id=str(agent.id)
                )

            await log_user_input_event()

            @database_sync_to_async
            def get_agent_name():
                return agent.agent_type.name

            agent_name = await get_agent_name()
            logger.info(f"User input requested by {agent_name}: {question}")

            return ToolResult(
                success=True,
                message="Question sent to user. Waiting for response.",
                data={
                    "message_id": str(message.id),
                    "question": question,
                    "options": options,
                    "status": "waiting"
                }
            )

        except Exception as e:
            logger.exception(f"Error asking user: {e}")
            return ToolResult(
                success=False,
                message=f"Error asking user: {str(e)}",
                error_code="ASK_ERROR"
            )


class HireAgentTool(BaseTool):
    """Hire a new agent to help with the project."""

    @property
    def name(self) -> str:
        return "hire_agent"

    @property
    def description(self) -> str:
        return "Hire a new agent to help with specific tasks. Only hire agents you have authority to hire."

    @property
    def parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "agent_type": {
                    "type": "string",
                    "description": "Type of agent to hire (e.g., 'backend_lead', 'frontend_lead')"
                },
                "purpose": {
                    "type": "string",
                    "description": "Why you're hiring this agent"
                },
                "initial_task_title": {
                    "type": "string",
                    "description": "Title of the first task for the new agent"
                },
                "initial_task_description": {
                    "type": "string",
                    "description": "Description of the first task"
                }
            },
            "required": ["agent_type", "purpose"]
        }

    async def execute(
        self,
        arguments: Dict[str, Any],
        context: Dict[str, Any]
    ) -> ToolResult:
        """Hire a new agent."""
        is_valid, error = self.validate_arguments(arguments)
        if not is_valid:
            return ToolResult(
                success=False,
                message=f"Invalid arguments: {error}",
                error_code="INVALID_ARGS"
            )

        agent_type_name = arguments["agent_type"]
        purpose = arguments["purpose"]
        initial_task_title = arguments.get("initial_task_title")
        initial_task_description = arguments.get("initial_task_description")

        project = context["project"]
        hiring_agent = context["agent"]

        try:
            # Check if hiring agent can hire this type
            @database_sync_to_async
            def check_authority():
                return hiring_agent.agent_type.can_hire or []

            can_hire = await check_authority()
            if agent_type_name not in can_hire:
                return ToolResult(
                    success=False,
                    message=f"You don't have authority to hire {agent_type_name}. You can hire: {', '.join(can_hire)}",
                    error_code="INSUFFICIENT_AUTHORITY"
                )

            # Get agent type
            @database_sync_to_async
            def get_agent_type():
                from apps.agents.models import AgentType
                return AgentType.objects.filter(role=agent_type_name).first()

            agent_type = await get_agent_type()

            if not agent_type:
                return ToolResult(
                    success=False,
                    message=f"Agent type not found: {agent_type_name}",
                    error_code="AGENT_TYPE_NOT_FOUND"
                )

            # Check subscription limits
            @database_sync_to_async
            def check_limits():
                current_agent_count = AgentInstance.objects.filter(project=project).count()
                max_agents = project.created_by.subscription.max_agents_per_project
                return current_agent_count, max_agents

            current_agent_count, max_agents = await check_limits()

            if current_agent_count >= max_agents:
                return ToolResult(
                    success=False,
                    message=f"Maximum agent limit reached ({max_agents}). Upgrade subscription to hire more agents.",
                    error_code="LIMIT_REACHED"
                )

            # Create agent instance
            @database_sync_to_async
            def create_agent():
                return AgentInstance.objects.create(
                    project=project,
                    agent_type=agent_type,
                    hired_by=hiring_agent,
                    model=hiring_agent.model,  # Inherit model from hiring agent
                    temperature=0.7,
                    status=AgentStatus.IDLE
                )

            new_agent = await create_agent()

            # Log event
            @database_sync_to_async
            def log_hire_event():
                EventStore.log_agent_hired(
                    project=project,
                    agent_type=agent_type_name,
                    agent_id=str(new_agent.id),
                    hired_by=str(hiring_agent.id)
                )

            await log_hire_event()

            # Create initial task if provided
            task_id = None
            if initial_task_title and initial_task_description:
                @database_sync_to_async
                def create_task():
                    from apps.tasks.models import Task
                    task = Task.objects.create(
                        project=project,
                        title=initial_task_title,
                        description=initial_task_description,
                        task_type='feature',
                        priority='medium',
                        created_by_agent=hiring_agent,
                        assigned_to_agent=new_agent
                    )
                    return str(task.id)

                task_id = await create_task()

            @database_sync_to_async
            def get_agent_names():
                return hiring_agent.agent_type.name, agent_type.name

            hiring_agent_name, new_agent_name = await get_agent_names()

            logger.info(
                f"Agent hired: {agent_type_name} by {hiring_agent_name} "
                f"for purpose: {purpose}"
            )

            return ToolResult(
                success=True,
                message=f"Successfully hired {new_agent_name}",
                data={
                    "agent_id": str(new_agent.id),
                    "agent_type": agent_type_name,
                    "agent_name": new_agent_name,
                    "purpose": purpose,
                    "initial_task_id": task_id
                },
                is_reversible=False  # Hiring is not easily reversible
            )

        except Exception as e:
            logger.exception(f"Error hiring agent: {e}")
            return ToolResult(
                success=False,
                message=f"Error hiring agent: {str(e)}",
                error_code="HIRE_ERROR"
            )
