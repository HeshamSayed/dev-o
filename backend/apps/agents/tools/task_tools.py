"""
Task Management Tools

Tools for creating, updating, and managing tasks.
These enable agents to break down work and coordinate.
"""

import logging
from typing import Dict, Any
from datetime import datetime
from channels.db import database_sync_to_async

from .base import BaseTool, ToolResult
from apps.tasks.models import Task, TaskStatus, TaskPriority, TaskDependency
from apps.context.services.event_store import EventStore

logger = logging.getLogger(__name__)


class CreateTaskTool(BaseTool):
    """Create a new task."""

    @property
    def name(self) -> str:
        return "create_task"

    @property
    def description(self) -> str:
        return "Create a new task. Use this to break down work or delegate to other agents."

    @property
    def parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Brief task title"
                },
                "description": {
                    "type": "string",
                    "description": "Detailed task description"
                },
                "task_type": {
                    "type": "string",
                    "description": "Task type: feature, bug_fix, refactor, documentation, testing, architecture",
                    "enum": ["feature", "bug_fix", "refactor", "documentation", "testing", "architecture"]
                },
                "priority": {
                    "type": "string",
                    "description": "Priority: low, medium, high, critical",
                    "enum": ["low", "medium", "high", "critical"]
                },
                "assigned_to_agent_id": {
                    "type": "string",
                    "description": "ID of agent to assign to (optional)"
                },
                "requirements": {
                    "type": "object",
                    "description": "Task requirements as key-value pairs"
                },
                "acceptance_criteria": {
                    "type": "array",
                    "description": "List of acceptance criteria",
                    "items": {"type": "string"}
                }
            },
            "required": ["title", "description", "task_type"]
        }

    async def execute(
        self,
        arguments: Dict[str, Any],
        context: Dict[str, Any]
    ) -> ToolResult:
        """Create new task."""
        is_valid, error = self.validate_arguments(arguments)
        if not is_valid:
            return ToolResult(
                success=False,
                message=f"Invalid arguments: {error}",
                error_code="INVALID_ARGS"
            )

        project = context["project"]
        agent = context["agent"]
        current_task = context.get("task")

        try:
            # Extract arguments
            title = arguments["title"]
            description = arguments["description"]
            task_type = arguments["task_type"]
            priority_str = arguments.get("priority", "medium")
            requirements = arguments.get("requirements", {})
            acceptance_criteria = arguments.get("acceptance_criteria", [])
            assigned_to_id = arguments.get("assigned_to_agent_id")

            # Convert priority string to integer
            priority_map = {
                "critical": TaskPriority.CRITICAL,  # 1
                "high": TaskPriority.HIGH,          # 2
                "medium": TaskPriority.MEDIUM,      # 3
                "low": TaskPriority.LOW             # 4
            }
            priority = priority_map.get(priority_str, TaskPriority.MEDIUM)

            # Create task and handle dependencies
            @database_sync_to_async
            def create_task_with_deps():
                # Create task
                task = Task.objects.create(
                    project=project,
                    title=title,
                    description=description,
                    task_type=task_type,
                    priority=priority,
                    requirements=requirements,
                    acceptance_criteria=acceptance_criteria,
                    parent_task=current_task  # Link to current task as subtask
                )

                # Assign if specified
                if assigned_to_id:
                    from apps.agents.models import AgentInstance
                    assigned_agent = AgentInstance.objects.filter(
                        id=assigned_to_id,
                        project=project
                    ).first()

                    if assigned_agent:
                        task.assigned_to = assigned_agent
                        task.save()

                # Create dependency if this is a subtask
                if current_task:
                    TaskDependency.objects.create(
                        task=task,
                        depends_on=current_task,
                        dependency_type='subtask'
                    )

                return task

            task = await create_task_with_deps()

            # Log event
            @database_sync_to_async
            def log_task_created_event():
                EventStore.log_task_created(
                    project=project,
                    task_id=str(task.id),
                    task_title=title,
                    created_by=str(agent.id)
                )

            await log_task_created_event()

            @database_sync_to_async
            def get_agent_name():
                return agent.agent_type.name

            agent_name = await get_agent_name()
            logger.info(f"Created task '{title}' by {agent_name}")

            @database_sync_to_async
            def get_task_status():
                return task.status

            task_status = await get_task_status()

            return ToolResult(
                success=True,
                message=f"Successfully created task: {title}",
                data={
                    "task_id": str(task.id),
                    "title": title,
                    "type": task_type,
                    "priority": priority,
                    "status": task_status
                },
                is_reversible=True,
                reverse_action={
                    "tool": "update_task_status",
                    "arguments": {
                        "task_id": str(task.id),
                        "status": "cancelled"
                    }
                }
            )

        except Exception as e:
            logger.exception(f"Error creating task: {e}")
            return ToolResult(
                success=False,
                message=f"Error creating task: {str(e)}",
                error_code="CREATE_ERROR"
            )


class UpdateTaskStatusTool(BaseTool):
    """Update task status."""

    @property
    def name(self) -> str:
        return "update_task_status"

    @property
    def description(self) -> str:
        return "Update the status of a task. Use this to mark tasks as completed, blocked, etc."

    @property
    def parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "string",
                    "description": "ID of the task to update"
                },
                "status": {
                    "type": "string",
                    "description": "New status",
                    "enum": ["pending", "in_progress", "blocked", "completed", "cancelled"]
                },
                "notes": {
                    "type": "string",
                    "description": "Notes about the status change"
                }
            },
            "required": ["task_id", "status"]
        }

    async def execute(
        self,
        arguments: Dict[str, Any],
        context: Dict[str, Any]
    ) -> ToolResult:
        """Update task status."""
        is_valid, error = self.validate_arguments(arguments)
        if not is_valid:
            return ToolResult(
                success=False,
                message=f"Invalid arguments: {error}",
                error_code="INVALID_ARGS"
            )

        task_id = arguments["task_id"]
        new_status = arguments["status"]
        notes = arguments.get("notes", "")

        project = context["project"]
        agent = context["agent"]

        try:
            # Get and update task
            @database_sync_to_async
            def update_task():
                # Get task
                task = Task.objects.filter(id=task_id, project=project).first()

                if not task:
                    return None, None, None

                # Store old status for reversal
                old_status = task.status

                # Update status
                task.status = new_status

                # Handle completed status
                if new_status == TaskStatus.COMPLETED:
                    task.completed_at = datetime.now()

                task.save()

                # Log to task log
                from apps.tasks.models import TaskLog
                TaskLog.objects.create(
                    task=task,
                    agent=agent,
                    log_type='status_change',
                    message=f"Status changed from {old_status} to {new_status}",
                    details={"notes": notes} if notes else {}
                )

                return task, old_status, task.title

            task, old_status, task_title = await update_task()

            if not task:
                return ToolResult(
                    success=False,
                    message=f"Task not found: {task_id}",
                    error_code="TASK_NOT_FOUND"
                )

            # Log completion event if completed
            if new_status == TaskStatus.COMPLETED:
                @database_sync_to_async
                def log_completion_event():
                    EventStore.log_task_completed(
                        project=project,
                        task_id=str(task.id),
                        task_title=task_title,
                        completed_by=str(agent.id)
                    )

                await log_completion_event()

            logger.info(f"Updated task {task_title} status: {old_status} → {new_status}")

            return ToolResult(
                success=True,
                message=f"Task status updated to {new_status}",
                data={
                    "task_id": str(task.id),
                    "old_status": old_status,
                    "new_status": new_status
                },
                is_reversible=True,
                reverse_action={
                    "tool": "update_task_status",
                    "arguments": {
                        "task_id": task_id,
                        "status": old_status
                    }
                }
            )

        except Exception as e:
            logger.exception(f"Error updating task status: {e}")
            return ToolResult(
                success=False,
                message=f"Error updating task: {str(e)}",
                error_code="UPDATE_ERROR"
            )


class AssignTaskTool(BaseTool):
    """Assign a task to an agent."""

    @property
    def name(self) -> str:
        return "assign_task"

    @property
    def description(self) -> str:
        return "Assign a task to a specific agent."

    @property
    def parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "string",
                    "description": "ID of the task to assign"
                },
                "agent_id": {
                    "type": "string",
                    "description": "ID of the agent to assign to"
                },
                "instructions": {
                    "type": "string",
                    "description": "Additional instructions for the assigned agent"
                }
            },
            "required": ["task_id", "agent_id"]
        }

    async def execute(
        self,
        arguments: Dict[str, Any],
        context: Dict[str, Any]
    ) -> ToolResult:
        """Assign task to agent."""
        is_valid, error = self.validate_arguments(arguments)
        if not is_valid:
            return ToolResult(
                success=False,
                message=f"Invalid arguments: {error}",
                error_code="INVALID_ARGS"
            )

        task_id = arguments["task_id"]
        agent_id = arguments["agent_id"]
        instructions = arguments.get("instructions", "")

        project = context["project"]
        current_agent = context["agent"]

        try:
            # Get task and agent, check authority, and assign
            @database_sync_to_async
            def assign_task_to_agent():
                # Get task and agent
                task = Task.objects.filter(id=task_id, project=project).first()
                if not task:
                    return None, "task_not_found", None, None, None

                from apps.agents.models import AgentInstance
                target_agent = AgentInstance.objects.filter(
                    id=agent_id,
                    project=project
                ).first()

                if not target_agent:
                    return None, "agent_not_found", None, None, None

                # Check if current agent has authority to assign
                # (Simplified - in production, check hierarchy)
                if current_agent.agent_type.hierarchy_level > target_agent.agent_type.hierarchy_level:
                    return None, "insufficient_authority", None, None, None

                # Store previous assignment
                previous_agent_id = str(task.assigned_to.id) if task.assigned_to else None

                # Assign task
                task.assigned_to = target_agent
                task.status = TaskStatus.PENDING
                task.save()

                # Log assignment
                from apps.tasks.models import TaskLog
                TaskLog.objects.create(
                    task=task,
                    agent=current_agent,
                    log_type='assignment',
                    message=f"Assigned to {target_agent.agent_type.name}",
                    details={"instructions": instructions} if instructions else {}
                )

                return task, "success", previous_agent_id, target_agent.agent_type.name, current_agent.agent_type.name

            task, status, previous_agent_id, target_agent_name, current_agent_name = await assign_task_to_agent()

            if status == "task_not_found":
                return ToolResult(
                    success=False,
                    message=f"Task not found: {task_id}",
                    error_code="TASK_NOT_FOUND"
                )
            elif status == "agent_not_found":
                return ToolResult(
                    success=False,
                    message=f"Agent not found: {agent_id}",
                    error_code="AGENT_NOT_FOUND"
                )
            elif status == "insufficient_authority":
                return ToolResult(
                    success=False,
                    message="Cannot assign tasks to higher-level agents",
                    error_code="INSUFFICIENT_AUTHORITY"
                )

            # Log event
            @database_sync_to_async
            def get_task_info():
                return task.id, task.title

            task_id_val, task_title = await get_task_info()

            @database_sync_to_async
            def log_assignment_event():
                EventStore.log_event(
                    project=project,
                    event_type='task_assigned',
                    event_data={
                        "task_id": str(task_id_val),
                        "task_title": task_title,
                        "assigned_to": agent_id,
                        "assigned_by": str(current_agent.id)
                    },
                    actor_type='agent',
                    actor_id=str(current_agent.id)
                )

            await log_assignment_event()

            logger.info(
                f"Task '{task_title}' assigned to {target_agent_name} "
                f"by {current_agent_name}"
            )

            return ToolResult(
                success=True,
                message=f"Task assigned to {target_agent_name}",
                data={
                    "task_id": str(task_id_val),
                    "assigned_to": agent_id,
                    "agent_type": target_agent_name
                },
                is_reversible=True,
                reverse_action={
                    "tool": "assign_task",
                    "arguments": {
                        "task_id": task_id,
                        "agent_id": previous_agent_id
                    }
                } if previous_agent_id else None
            )

        except Exception as e:
            logger.exception(f"Error assigning task: {e}")
            return ToolResult(
                success=False,
                message=f"Error assigning task: {str(e)}",
                error_code="ASSIGN_ERROR"
            )
