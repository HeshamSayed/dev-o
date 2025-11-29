"""
Project Models

Design Decisions:
1. Projects contain all configuration and state
2. Project manifest stores structured requirements and architecture
3. Support for Git integration
4. Checkpoints for recovery and undo
"""

from django.db import models
from core.mixins import UUIDPrimaryKeyMixin, TimestampMixin


class ProjectStatus(models.TextChoices):
    """Project status choices."""
    INITIALIZING = 'initializing', 'Initializing'
    PLANNING = 'planning', 'Planning'
    IN_PROGRESS = 'in_progress', 'In Progress'
    REVIEW = 'review', 'Review'
    COMPLETED = 'completed', 'Completed'
    PAUSED = 'paused', 'Paused'
    ARCHIVED = 'archived', 'Archived'


class Project(UUIDPrimaryKeyMixin, TimestampMixin):
    """Main project entity"""

    owner = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='projects'
    )

    # Basic info
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=ProjectStatus.choices,
        default=ProjectStatus.INITIALIZING,
        db_index=True
    )

    # Project manifest (structured data)
    manifest = models.JSONField(default=dict, blank=True)
    # Structure:
    # {
    #     "requirements": {
    #         "functional": [...],
    #         "non_functional": [...],
    #         "user_stories": [...]
    #     },
    #     "domain_model": {
    #         "entities": [...],
    #         "relationships": [...]
    #     },
    #     "tech_stack": {
    #         "backend": "Django + DRF",
    #         "frontend": "React",
    #         "database": "PostgreSQL",
    #         ...
    #     },
    #     "architecture": {
    #         "type": "monolith",
    #         "components": [...],
    #         "apis": [...]
    #     }
    # }

    # Configuration
    settings = models.JSONField(default=dict, blank=True)
    # Structure:
    # {
    #     "llm_model": "deepseek-r1:7b",
    #     "auto_test": true,
    #     "code_style": "black",
    #     "test_framework": "pytest",
    #     ...
    # }

    # Git integration
    repository_url = models.URLField(blank=True, null=True)
    repository_branch = models.CharField(max_length=100, default='main')
    last_commit_sha = models.CharField(max_length=40, blank=True, null=True)

    # Local path (for CLI)
    local_path = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'projects'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['owner', 'status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['name']),
        ]
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return f"{self.name} ({self.owner.email})"

    def get_file_tree(self):
        """Get project file tree"""
        from apps.code.models import CodeArtifact
        files = CodeArtifact.objects.filter(
            project=self
        ).values_list('file_path', flat=True)
        return self._build_tree(list(files))

    def _build_tree(self, paths):
        """Build tree structure from flat paths"""
        tree = {}
        for path in paths:
            parts = path.split('/')
            current = tree
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = None  # File (leaf)
        return tree

    def get_stats(self):
        """Get project statistics."""
        from apps.tasks.models import Task
        from apps.code.models import CodeArtifact
        from apps.agents.models import AgentInstance

        return {
            'total_tasks': Task.objects.filter(project=self).count(),
            'completed_tasks': Task.objects.filter(
                project=self,
                status='completed'
            ).count(),
            'total_files': CodeArtifact.objects.filter(project=self).count(),
            'total_lines': sum(
                CodeArtifact.objects.filter(project=self).values_list(
                    'line_count',
                    flat=True
                )
            ),
            'active_agents': AgentInstance.objects.filter(
                project=self,
                status__in=['working', 'waiting_input']
            ).count(),
        }


class ProjectCheckpoint(UUIDPrimaryKeyMixin, TimestampMixin):
    """Checkpoint for recovery and undo"""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='checkpoints'
    )

    # Checkpoint data
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    # Full state snapshot
    state_snapshot = models.JSONField()
    # Structure:
    # {
    #     "manifest": {...},
    #     "agents": [...],
    #     "tasks": [...],
    #     "files": {...}  # file_path -> content_hash mapping
    # }

    # Metadata
    created_by = models.CharField(max_length=100)  # 'user' or agent_id
    is_auto = models.BooleanField(default=False)  # Auto-checkpoint vs manual

    class Meta:
        db_table = 'project_checkpoints'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['project', 'created_at']),
        ]
        verbose_name = 'Project Checkpoint'
        verbose_name_plural = 'Project Checkpoints'

    def __str__(self):
        return f"{self.project.name} - {self.name}"
