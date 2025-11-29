"""
Context and Memory Models

Design Decisions:
1. Multiple memory types for different purposes
2. Vector storage for semantic retrieval
3. Decision tracking for architecture consistency
4. Event log for full traceability
"""

from django.db import models
from pgvector.django import VectorField
from core.mixins import UUIDPrimaryKeyMixin, TimestampMixin


class MemoryType(models.TextChoices):
    """Memory type choices."""
    REQUIREMENT = 'requirement', 'Requirement'
    DECISION = 'decision', 'Decision'
    ARCHITECTURE = 'architecture', 'Architecture'
    CODE_PATTERN = 'code_pattern', 'Code Pattern'
    ERROR_RESOLUTION = 'error_resolution', 'Error Resolution'
    CONVERSATION = 'conversation', 'Conversation'
    LEARNING = 'learning', 'Learning'


class Memory(UUIDPrimaryKeyMixin, TimestampMixin):
    """Long-term memory storage with vector search"""

    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='memories'
    )

    # Memory classification
    memory_type = models.CharField(
        max_length=20,
        choices=MemoryType.choices,
        db_index=True
    )

    # Content
    title = models.CharField(max_length=500)
    content = models.TextField()

    # Vector embedding
    embedding = VectorField(dimensions=1536)

    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    # Structure varies by type

    # Context
    created_by_agent = models.ForeignKey(
        'agents.AgentInstance',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    related_task = models.ForeignKey(
        'tasks.Task',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Importance for retrieval ranking
    importance = models.FloatField(default=0.5)
    access_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'memories'
        indexes = [
            models.Index(fields=['project', 'memory_type']),
            models.Index(fields=['importance']),
        ]
        verbose_name = 'Memory'
        verbose_name_plural = 'Memories'

    def __str__(self):
        return f"{self.memory_type}: {self.title}"


class Decision(UUIDPrimaryKeyMixin, TimestampMixin):
    """Architectural and design decisions"""

    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='decisions'
    )

    # Decision details
    decision_type = models.CharField(max_length=100, db_index=True)
    # Types: architecture, tech_choice, design_pattern, api_design,
    #        database_schema, naming_convention, etc.

    title = models.CharField(max_length=500)
    description = models.TextField()
    reasoning = models.TextField()

    # Alternatives considered
    alternatives = models.JSONField(default=list, blank=True)
    # [{"option": "...", "pros": [...], "cons": [...], "rejected_reason": "..."}]

    # Impact
    affected_components = models.JSONField(default=list, blank=True)
    # ["users", "api", "database"]

    # Context
    made_by_agent = models.ForeignKey(
        'agents.AgentInstance',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    related_task = models.ForeignKey(
        'tasks.Task',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Vector embedding for retrieval
    embedding = VectorField(dimensions=1536, null=True, blank=True)

    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('proposed', 'Proposed'),
            ('approved', 'Approved'),
            ('implemented', 'Implemented'),
            ('superseded', 'Superseded'),
        ],
        default='approved',
        db_index=True
    )
    superseded_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'decisions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['project', 'status']),
            models.Index(fields=['decision_type']),
        ]
        verbose_name = 'Decision'
        verbose_name_plural = 'Decisions'

    def __str__(self):
        return f"{self.decision_type}: {self.title}"


class EventLog(UUIDPrimaryKeyMixin, TimestampMixin):
    """Complete event log for the project (event sourcing)"""

    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='events'
    )

    # Event identification
    event_type = models.CharField(max_length=100, db_index=True)
    # Types: project_created, agent_hired, task_created, task_assigned,
    #        task_completed, file_created, file_modified, decision_made,
    #        error_occurred, user_input, checkpoint_created, etc.

    # Event data
    event_data = models.JSONField()

    # Actor
    actor_type = models.CharField(max_length=20)  # 'agent', 'user', 'system'
    actor_id = models.CharField(max_length=100, blank=True)

    # Sequence for ordering
    sequence_number = models.BigIntegerField(db_index=True)

    class Meta:
        db_table = 'event_log'
        ordering = ['sequence_number']
        indexes = [
            models.Index(fields=['project', 'sequence_number']),
            models.Index(fields=['event_type']),
            models.Index(fields=['created_at']),
        ]
        verbose_name = 'Event Log'
        verbose_name_plural = 'Event Logs'

    def __str__(self):
        return f"[{self.sequence_number}] {self.event_type}"
