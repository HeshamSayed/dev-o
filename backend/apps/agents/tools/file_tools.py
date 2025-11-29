"""
File Tools

Tools for file operations: read, write, modify, delete.
These tools interact with the codebase and track changes.
"""

import os
import logging
from typing import Dict, Any
from pathlib import Path
from channels.db import database_sync_to_async

from .base import BaseTool, ToolResult
from apps.code.models import CodeArtifact, CodeChange
from apps.context.services.event_store import EventStore
from apps.context.services.artifact_registry import ArtifactRegistryService

logger = logging.getLogger(__name__)


class ReadFileTool(BaseTool):
    """Read contents of a file."""

    @property
    def name(self) -> str:
        return "read_file"

    @property
    def description(self) -> str:
        return "Read the contents of a file from the project codebase."

    @property
    def parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file relative to project root"
                }
            },
            "required": ["file_path"]
        }

    async def execute(
        self,
        arguments: Dict[str, Any],
        context: Dict[str, Any]
    ) -> ToolResult:
        """Read file contents."""
        # Validate arguments
        is_valid, error = self.validate_arguments(arguments)
        if not is_valid:
            return ToolResult(
                success=False,
                message=f"Invalid arguments: {error}",
                error_code="INVALID_ARGS"
            )

        file_path = arguments["file_path"]
        project = context["project"]

        # Check if file exists in artifacts
        try:
            @database_sync_to_async
            def get_artifact():
                return CodeArtifact.objects.filter(
                    project=project,
                    file_path=file_path
                ).first()

            artifact = await get_artifact()

            if artifact:
                @database_sync_to_async
                def get_artifact_data():
                    return artifact.content, artifact.language

                content, language = await get_artifact_data()

                logger.info(f"Read file from artifacts: {file_path}")
                return ToolResult(
                    success=True,
                    message=f"Successfully read {file_path}",
                    data={
                        "file_path": file_path,
                        "content": content,
                        "language": language,
                        "lines": len(content.splitlines())
                    }
                )

            # Try reading from filesystem
            @database_sync_to_async
            def get_project_root():
                return project.root_directory

            project_root = await get_project_root()
            full_path = Path(project_root) / file_path if project_root else Path(file_path)

            if full_path.exists() and full_path.is_file():
                content = full_path.read_text(encoding='utf-8')

                logger.info(f"Read file from filesystem: {file_path}")
                return ToolResult(
                    success=True,
                    message=f"Successfully read {file_path}",
                    data={
                        "file_path": file_path,
                        "content": content,
                        "lines": len(content.splitlines())
                    }
                )

            return ToolResult(
                success=False,
                message=f"File not found: {file_path}",
                error_code="FILE_NOT_FOUND"
            )

        except Exception as e:
            logger.exception(f"Error reading file {file_path}: {e}")
            return ToolResult(
                success=False,
                message=f"Error reading file: {str(e)}",
                error_code="READ_ERROR"
            )


class WriteFileTool(BaseTool):
    """Create a new file."""

    @property
    def name(self) -> str:
        return "write_file"

    @property
    def description(self) -> str:
        return "Create a new file with the given content. Will fail if file already exists."

    @property
    def parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path for the new file relative to project root"
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file"
                },
                "description": {
                    "type": "string",
                    "description": "Description of what this file does"
                }
            },
            "required": ["file_path", "content"]
        }

    async def execute(
        self,
        arguments: Dict[str, Any],
        context: Dict[str, Any]
    ) -> ToolResult:
        """Create new file."""
        is_valid, error = self.validate_arguments(arguments)
        if not is_valid:
            return ToolResult(
                success=False,
                message=f"Invalid arguments: {error}",
                error_code="INVALID_ARGS"
            )

        file_path = arguments["file_path"]
        content = arguments["content"]
        description = arguments.get("description", "")

        project = context["project"]
        agent = context["agent"]
        task = context.get("task")

        try:
            # Check if file already exists
            @database_sync_to_async
            def check_file_exists():
                return CodeArtifact.objects.filter(project=project, file_path=file_path).exists()

            if await check_file_exists():
                return ToolResult(
                    success=False,
                    message=f"File already exists: {file_path}. Use modify_file to update it.",
                    error_code="FILE_EXISTS"
                )

            # Determine language from extension
            ext = Path(file_path).suffix.lstrip('.')
            language = ext if ext else "text"

            # Create artifact and log change
            @database_sync_to_async
            def create_artifact_and_change():
                # Create artifact
                artifact = CodeArtifact.objects.create(
                    project=project,
                    file_path=file_path,
                    content=content,
                    language=language,
                    created_by_agent=agent,
                    created_by_task=task
                )

                # Log change
                CodeChange.objects.create(
                    artifact=artifact,
                    change_type='create',
                    diff=content,
                    agent=agent,
                    task=task,
                    description=description or f"Created {file_path}"
                )

                return artifact

            artifact = await create_artifact_and_change()

            # Log event
            @database_sync_to_async
            def log_file_created_event():
                EventStore.log_file_created(
                    project=project,
                    file_path=file_path,
                    created_by=str(agent.id)
                )

            await log_file_created_event()

            @database_sync_to_async
            def get_agent_name():
                return agent.agent_type.name

            agent_name = await get_agent_name()
            logger.info(f"Created file: {file_path} by {agent_name}")

            return ToolResult(
                success=True,
                message=f"Successfully created {file_path}",
                data={
                    "file_path": file_path,
                    "lines": len(content.splitlines()),
                    "artifact_id": str(artifact.id)
                },
                is_reversible=True,
                reverse_action={
                    "tool": "delete_file",
                    "arguments": {"file_path": file_path}
                }
            )

        except Exception as e:
            logger.exception(f"Error creating file {file_path}: {e}")
            return ToolResult(
                success=False,
                message=f"Error creating file: {str(e)}",
                error_code="WRITE_ERROR"
            )


class ModifyFileTool(BaseTool):
    """Modify an existing file."""

    @property
    def name(self) -> str:
        return "modify_file"

    @property
    def description(self) -> str:
        return "Modify an existing file. Provide the complete new content."

    @property
    def parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to modify"
                },
                "content": {
                    "type": "string",
                    "description": "New content for the file"
                },
                "description": {
                    "type": "string",
                    "description": "Description of the changes made"
                }
            },
            "required": ["file_path", "content"]
        }

    async def execute(
        self,
        arguments: Dict[str, Any],
        context: Dict[str, Any]
    ) -> ToolResult:
        """Modify existing file."""
        is_valid, error = self.validate_arguments(arguments)
        if not is_valid:
            return ToolResult(
                success=False,
                message=f"Invalid arguments: {error}",
                error_code="INVALID_ARGS"
            )

        file_path = arguments["file_path"]
        new_content = arguments["content"]
        description = arguments.get("description", "")

        project = context["project"]
        agent = context["agent"]
        task = context.get("task")

        try:
            # Get existing artifact
            artifact = CodeArtifact.objects.filter(
                project=project,
                file_path=file_path
            ).first()

            if not artifact:
                return ToolResult(
                    success=False,
                    message=f"File not found: {file_path}. Use write_file to create it.",
                    error_code="FILE_NOT_FOUND"
                )

            # Store old content for diff
            old_content = artifact.content

            # Generate diff (simplified - in production use difflib)
            old_lines = len(old_content.splitlines())
            new_lines = len(new_content.splitlines())
            diff_summary = f"Modified {file_path}: {old_lines} → {new_lines} lines"

            # Update artifact
            artifact.content = new_content
            artifact.save()

            # Log change
            CodeChange.objects.create(
                artifact=artifact,
                change_type='modify',
                diff=diff_summary,
                agent=agent,
                task=task,
                description=description or f"Modified {file_path}"
            )

            # Log event
            EventStore.log_event(
                project=project,
                event_type='file_modified',
                event_data={
                    "file_path": file_path,
                    "old_lines": old_lines,
                    "new_lines": new_lines
                },
                actor_type='agent',
                actor_id=str(agent.id)
            )

            logger.info(f"Modified file: {file_path} by {agent.agent_type.name}")

            return ToolResult(
                success=True,
                message=f"Successfully modified {file_path}",
                data={
                    "file_path": file_path,
                    "old_lines": old_lines,
                    "new_lines": new_lines
                },
                is_reversible=True,
                reverse_action={
                    "tool": "modify_file",
                    "arguments": {
                        "file_path": file_path,
                        "content": old_content
                    }
                }
            )

        except Exception as e:
            logger.exception(f"Error modifying file {file_path}: {e}")
            return ToolResult(
                success=False,
                message=f"Error modifying file: {str(e)}",
                error_code="MODIFY_ERROR"
            )


class DeleteFileTool(BaseTool):
    """Delete a file."""

    @property
    def name(self) -> str:
        return "delete_file"

    @property
    def description(self) -> str:
        return "Delete a file from the project. Use with caution."

    @property
    def parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to delete"
                },
                "reason": {
                    "type": "string",
                    "description": "Reason for deletion"
                }
            },
            "required": ["file_path", "reason"]
        }

    async def execute(
        self,
        arguments: Dict[str, Any],
        context: Dict[str, Any]
    ) -> ToolResult:
        """Delete file."""
        is_valid, error = self.validate_arguments(arguments)
        if not is_valid:
            return ToolResult(
                success=False,
                message=f"Invalid arguments: {error}",
                error_code="INVALID_ARGS"
            )

        file_path = arguments["file_path"]
        reason = arguments["reason"]

        project = context["project"]
        agent = context["agent"]
        task = context.get("task")

        try:
            # Get artifact
            artifact = CodeArtifact.objects.filter(
                project=project,
                file_path=file_path
            ).first()

            if not artifact:
                return ToolResult(
                    success=False,
                    message=f"File not found: {file_path}",
                    error_code="FILE_NOT_FOUND"
                )

            # Store content for potential reversal
            old_content = artifact.content

            # Soft delete (mark as inactive)
            artifact.is_active = False
            artifact.save()

            # Log change
            CodeChange.objects.create(
                artifact=artifact,
                change_type='delete',
                diff=f"Deleted {file_path}",
                agent=agent,
                task=task,
                description=reason
            )

            # Log event
            EventStore.log_event(
                project=project,
                event_type='file_deleted',
                event_data={
                    "file_path": file_path,
                    "reason": reason
                },
                actor_type='agent',
                actor_id=str(agent.id)
            )

            logger.info(f"Deleted file: {file_path} by {agent.agent_type.name}")

            return ToolResult(
                success=True,
                message=f"Successfully deleted {file_path}",
                data={"file_path": file_path},
                is_reversible=True,
                reverse_action={
                    "tool": "write_file",
                    "arguments": {
                        "file_path": file_path,
                        "content": old_content
                    }
                }
            )

        except Exception as e:
            logger.exception(f"Error deleting file {file_path}: {e}")
            return ToolResult(
                success=False,
                message=f"Error deleting file: {str(e)}",
                error_code="DELETE_ERROR"
            )
