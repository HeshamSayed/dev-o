"""
Code Artifact Models

Design Decisions:
1. Track all code files with content and metadata
2. Version history through CodeChange
3. Artifact registry for context sharing
4. Vector embeddings for semantic search
"""

import hashlib
from django.db import models
from pgvector.django import VectorField
from core.mixins import UUIDPrimaryKeyMixin, TimestampMixin


class CodeArtifact(UUIDPrimaryKeyMixin, TimestampMixin):
    """Code artifact (file) in the project"""

    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='code_artifacts'
    )

    # File info
    file_path = models.CharField(max_length=500, db_index=True)
    file_name = models.CharField(max_length=255)
    language = models.CharField(max_length=50, blank=True)

    # Content
    content = models.TextField()
    content_hash = models.CharField(max_length=64, db_index=True)  # SHA-256
    line_count = models.IntegerField(default=0)

    # Vector embedding for semantic search
    embedding = VectorField(dimensions=1536, null=True, blank=True)

    # Metadata
    last_modified_by = models.ForeignKey(
        'agents.AgentInstance',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='modified_files'
    )
    last_modified_task = models.ForeignKey(
        'tasks.Task',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Parsed structure (for code understanding)
    structure = models.JSONField(default=dict, blank=True)
    # Structure for Python:
    # {
    #     "imports": [...],
    #     "classes": [
    #         {"name": "User", "methods": [...], "attributes": [...]}
    #     ],
    #     "functions": [...],
    #     "variables": [...]
    # }

    class Meta:
        db_table = 'code_artifacts'
        unique_together = ['project', 'file_path']
        indexes = [
            models.Index(fields=['project', 'file_path']),
            models.Index(fields=['language']),
            models.Index(fields=['content_hash']),
        ]
        verbose_name = 'Code Artifact'
        verbose_name_plural = 'Code Artifacts'

    def __str__(self):
        return f"{self.project.name}: {self.file_path}"

    def save(self, *args, **kwargs):
        """Override save to compute hash and line count."""
        self.content_hash = hashlib.sha256(self.content.encode()).hexdigest()
        self.line_count = len(self.content.split('\n'))
        self.file_name = self.file_path.split('/')[-1]
        super().save(*args, **kwargs)

    def get_size_bytes(self):
        """Get file size in bytes."""
        return len(self.content.encode('utf-8'))


class CodeChange(UUIDPrimaryKeyMixin, TimestampMixin):
    """History of changes to code artifacts"""

    artifact = models.ForeignKey(
        CodeArtifact,
        on_delete=models.CASCADE,
        related_name='changes'
    )

    # Change info
    change_type = models.CharField(
        max_length=20,
        choices=[
            ('created', 'Created'),
            ('modified', 'Modified'),
            ('deleted', 'Deleted'),
            ('renamed', 'Renamed'),
        ],
        db_index=True
    )

    # Content before/after
    content_before = models.TextField(blank=True)
    content_after = models.TextField()

    # Diff
    diff = models.TextField(blank=True)

    # Context
    agent = models.ForeignKey(
        'agents.AgentInstance',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    task = models.ForeignKey(
        'tasks.Task',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Reason for change
    reason = models.TextField(blank=True)

    class Meta:
        db_table = 'code_changes'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['artifact', 'created_at']),
        ]
        verbose_name = 'Code Change'
        verbose_name_plural = 'Code Changes'

    def __str__(self):
        return f"{self.artifact.file_path}: {self.change_type}"


class ArtifactRegistry(UUIDPrimaryKeyMixin, TimestampMixin):
    """Registry of all created artifacts for context sharing"""

    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='artifact_registry'
    )

    # Artifact identification
    artifact_type = models.CharField(max_length=50, db_index=True)
    # Types: model, serializer, view, url_pattern, api_endpoint,
    #        component, service, utility, test, migration, etc.

    name = models.CharField(max_length=255, db_index=True)

    # Location
    file_path = models.CharField(max_length=500)
    line_start = models.IntegerField(null=True, blank=True)
    line_end = models.IntegerField(null=True, blank=True)

    # Details
    details = models.JSONField(default=dict, blank=True)
    # Structure varies by type:
    # model: {"fields": [...], "relationships": [...], "methods": [...]}
    # api_endpoint: {"method": "POST", "path": "/api/users/", "request": {...}, "response": {...}}

    # Relations
    created_by_agent = models.ForeignKey(
        'agents.AgentInstance',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_by_task = models.ForeignKey(
        'tasks.Task',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Dependencies (what this artifact uses)
    dependencies = models.JSONField(default=list, blank=True)
    # List of artifact IDs this depends on

    # Embedding for semantic search
    embedding = VectorField(dimensions=1536, null=True, blank=True)

    # Status
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = 'artifact_registry'
        indexes = [
            models.Index(fields=['project', 'artifact_type']),
            models.Index(fields=['name']),
        ]
        verbose_name = 'Artifact Registry'
        verbose_name_plural = 'Artifact Registries'

    def __str__(self):
        return f"{self.artifact_type}: {self.name}"
