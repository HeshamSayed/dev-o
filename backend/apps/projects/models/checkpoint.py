"""
Project Checkpoint Model

Checkpoint for recovery and undo functionality.
"""

from django.db import models
from core.mixins import UUIDPrimaryKeyMixin, TimestampMixin


class ProjectCheckpoint(UUIDPrimaryKeyMixin, TimestampMixin):
    """Checkpoint for recovery and undo"""

    project = models.ForeignKey(
        'projects.Project',
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
