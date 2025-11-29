"""
Artifact Registry Service

Manages the registry of all created artifacts for context sharing.
This is critical for agents to know what other agents have created.
"""

import logging
from typing import Dict, Any, List, Optional
from django.db import transaction

from apps.code.models import ArtifactRegistry
from apps.projects.models import Project
from apps.agents.models import AgentInstance
from apps.tasks.models import Task

logger = logging.getLogger(__name__)


class ArtifactRegistryService:
    """
    Service for managing artifact registry.

    The artifact registry tracks all created artifacts so agents can:
    1. Know what has been created
    2. Find dependencies
    3. Share context about artifacts
    """

    @staticmethod
    @transaction.atomic
    def register_artifact(
        project: Project,
        artifact_type: str,
        name: str,
        file_path: str,
        details: Dict[str, Any],
        created_by_agent: Optional[AgentInstance] = None,
        created_by_task: Optional[Task] = None,
        dependencies: Optional[List[str]] = None,
        line_start: Optional[int] = None,
        line_end: Optional[int] = None,
    ) -> ArtifactRegistry:
        """
        Register a new artifact.

        Args:
            project: Project
            artifact_type: Type (model, serializer, view, etc.)
            name: Artifact name
            file_path: File path
            details: Type-specific details
            created_by_agent: Agent that created it
            created_by_task: Task it was created for
            dependencies: List of artifact IDs this depends on
            line_start: Starting line number
            line_end: Ending line number

        Returns:
            Created ArtifactRegistry instance
        """
        artifact = ArtifactRegistry.objects.create(
            project=project,
            artifact_type=artifact_type,
            name=name,
            file_path=file_path,
            line_start=line_start,
            line_end=line_end,
            details=details,
            created_by_agent=created_by_agent,
            created_by_task=created_by_task,
            dependencies=dependencies or [],
            is_active=True
        )

        logger.info(
            f"Registered artifact: {artifact_type}/{name} in {file_path} "
            f"by {created_by_agent.agent_type.name if created_by_agent else 'unknown'}"
        )

        return artifact

    @staticmethod
    def find_artifacts(
        project: Project,
        artifact_type: Optional[str] = None,
        name: Optional[str] = None,
        file_path: Optional[str] = None,
        is_active: bool = True
    ) -> List[ArtifactRegistry]:
        """
        Find artifacts matching criteria.

        Args:
            project: Project
            artifact_type: Filter by type
            name: Filter by name (partial match)
            file_path: Filter by file path (partial match)
            is_active: Filter by active status

        Returns:
            List of matching artifacts
        """
        queryset = ArtifactRegistry.objects.filter(
            project=project,
            is_active=is_active
        )

        if artifact_type:
            queryset = queryset.filter(artifact_type=artifact_type)

        if name:
            queryset = queryset.filter(name__icontains=name)

        if file_path:
            queryset = queryset.filter(file_path__icontains=file_path)

        return list(queryset.select_related(
            'created_by_agent',
            'created_by_task'
        ))

    @staticmethod
    def get_artifact(
        project: Project,
        artifact_type: str,
        name: str
    ) -> Optional[ArtifactRegistry]:
        """
        Get a specific artifact.

        Args:
            project: Project
            artifact_type: Artifact type
            name: Artifact name

        Returns:
            ArtifactRegistry instance or None
        """
        try:
            return ArtifactRegistry.objects.get(
                project=project,
                artifact_type=artifact_type,
                name=name,
                is_active=True
            )
        except ArtifactRegistry.DoesNotExist:
            return None

    @staticmethod
    def get_dependencies(artifact: ArtifactRegistry) -> List[ArtifactRegistry]:
        """
        Get all artifacts this artifact depends on.

        Args:
            artifact: Artifact to get dependencies for

        Returns:
            List of dependency artifacts
        """
        if not artifact.dependencies:
            return []

        return list(ArtifactRegistry.objects.filter(
            id__in=artifact.dependencies,
            is_active=True
        ))

    @staticmethod
    def get_dependents(artifact: ArtifactRegistry) -> List[ArtifactRegistry]:
        """
        Get all artifacts that depend on this artifact.

        Args:
            artifact: Artifact to get dependents for

        Returns:
            List of dependent artifacts
        """
        return list(ArtifactRegistry.objects.filter(
            dependencies__contains=[str(artifact.id)],
            is_active=True
        ))

    @staticmethod
    @transaction.atomic
    def update_artifact(
        artifact: ArtifactRegistry,
        details: Optional[Dict[str, Any]] = None,
        dependencies: Optional[List[str]] = None,
        line_start: Optional[int] = None,
        line_end: Optional[int] = None,
    ) -> ArtifactRegistry:
        """
        Update an existing artifact.

        Args:
            artifact: Artifact to update
            details: Updated details
            dependencies: Updated dependencies
            line_start: Updated start line
            line_end: Updated end line

        Returns:
            Updated artifact
        """
        if details is not None:
            artifact.details = details

        if dependencies is not None:
            artifact.dependencies = dependencies

        if line_start is not None:
            artifact.line_start = line_start

        if line_end is not None:
            artifact.line_end = line_end

        artifact.save()

        logger.info(f"Updated artifact: {artifact.artifact_type}/{artifact.name}")

        return artifact

    @staticmethod
    @transaction.atomic
    def deactivate_artifact(artifact: ArtifactRegistry) -> None:
        """
        Deactivate an artifact (soft delete).

        Args:
            artifact: Artifact to deactivate
        """
        artifact.is_active = False
        artifact.save()

        logger.info(f"Deactivated artifact: {artifact.artifact_type}/{artifact.name}")

    @staticmethod
    def get_project_artifacts_summary(project: Project) -> Dict[str, Any]:
        """
        Get summary of all artifacts in a project.

        Args:
            project: Project

        Returns:
            Summary dictionary with counts by type
        """
        artifacts = ArtifactRegistry.objects.filter(
            project=project,
            is_active=True
        )

        summary = {
            "total": artifacts.count(),
            "by_type": {}
        }

        for artifact in artifacts:
            artifact_type = artifact.artifact_type
            if artifact_type not in summary["by_type"]:
                summary["by_type"][artifact_type] = 0
            summary["by_type"][artifact_type] += 1

        return summary
