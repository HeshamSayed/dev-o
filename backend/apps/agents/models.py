"""
Agent Models

Design Decisions:
1. AgentType defines the template (persona, tools, hierarchy)
2. AgentInstance is the actual agent working on a project
3. AgentState tracks real-time state for recovery
4. AgentMessage enables inter-agent communication
5. AgentAction logs all actions for event sourcing
"""

from django.db import models
from django.contrib.postgres.fields import ArrayField
from core.mixins import UUIDPrimaryKeyMixin, TimestampMixin


class AgentHierarchyLevel(models.IntegerChoices):
    """Agent hierarchy levels."""
    ORCHESTRATOR = 0, 'Orchestrator'
    ARCHITECT = 1, 'Architect'
    LEAD = 2, 'Lead'
    SENIOR = 3, 'Senior'
    JUNIOR = 4, 'Junior'


class AgentType(UUIDPrimaryKeyMixin):
    """Template for agent types"""

    # Identity
    name = models.CharField(max_length=100, unique=True, db_index=True)
    role = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.TextField()

    # Persona
    system_prompt = models.TextField()

    # Capabilities
    available_tools = ArrayField(
        models.CharField(max_length=50),
        default=list,
        blank=True
    )
    can_hire = ArrayField(
        models.CharField(max_length=50),
        default=list,
        blank=True
    )

    # Hierarchy
    hierarchy_level = models.IntegerField(
        choices=AgentHierarchyLevel.choices,
        default=AgentHierarchyLevel.SENIOR
    )

    # Configuration
    default_model = models.CharField(max_length=50, default='deepseek-r1:7b')
    default_temperature = models.FloatField(default=0.7)
    max_iterations = models.IntegerField(default=50)

    # Status
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = 'agent_types'
        ordering = ['hierarchy_level', 'name']
        verbose_name = 'Agent Type'
        verbose_name_plural = 'Agent Types'

    def __str__(self):
        return f"{self.name} (Level {self.hierarchy_level})"


class AgentStatus(models.TextChoices):
    """Agent status choices."""
    IDLE = 'idle', 'Idle'
    WORKING = 'working', 'Working'
    WAITING_INPUT = 'waiting_input', 'Waiting for Input'
    WAITING_DEPENDENCY = 'waiting_dependency', 'Waiting for Dependency'
    BLOCKED = 'blocked', 'Blocked'
    ERROR = 'error', 'Error'
    COMPLETED = 'completed', 'Completed'


class AgentInstance(UUIDPrimaryKeyMixin, TimestampMixin):
    """Active agent instance working on a project"""

    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='agents'
    )
    agent_type = models.ForeignKey(
        AgentType,
        on_delete=models.PROTECT,
        related_name='instances'
    )

    # Hierarchy
    hired_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='hired_agents'
    )

    # Status
    status = models.CharField(
        max_length=20,
        choices=AgentStatus.choices,
        default=AgentStatus.IDLE,
        db_index=True
    )
    status_message = models.TextField(blank=True)

    # Current work
    current_task = models.ForeignKey(
        'tasks.Task',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_agents'
    )

    # Configuration overrides
    custom_instructions = models.TextField(blank=True)
    model_override = models.CharField(max_length=50, blank=True)
    temperature_override = models.FloatField(null=True, blank=True)

    # Working memory (short-term state)
    working_memory = models.JSONField(default=dict, blank=True)
    # Structure:
    # {
    #     "current_focus": "implementing user model",
    #     "files_in_progress": ["models.py"],
    #     "decisions_pending": [...],
    #     "notes": [...],
    #     "tool_calls": [...]
    # }

    # Conversation history (last N messages for context)
    conversation_history = models.JSONField(default=list, blank=True)

    # Statistics
    tasks_completed = models.IntegerField(default=0)
    errors_encountered = models.IntegerField(default=0)
    total_tokens_used = models.IntegerField(default=0)

    # Timestamps
    last_active_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'agent_instances'
        indexes = [
            models.Index(fields=['project', 'status']),
            models.Index(fields=['agent_type']),
            models.Index(fields=['last_active_at']),
        ]
        verbose_name = 'Agent Instance'
        verbose_name_plural = 'Agent Instances'

    def __str__(self):
        return f"{self.agent_type.name} @ {self.project.name}"

    @property
    def model(self):
        """Get model (with override support)."""
        return self.model_override or self.agent_type.default_model

    @property
    def temperature(self):
        """Get temperature (with override support)."""
        return self.temperature_override or self.agent_type.default_temperature


class AgentMessageType(models.TextChoices):
    """Agent message type choices."""
    TASK_ASSIGNMENT = 'task_assignment', 'Task Assignment'
    QUESTION = 'question', 'Question'
    ANSWER = 'answer', 'Answer'
    STATUS_UPDATE = 'status_update', 'Status Update'
    REVIEW_REQUEST = 'review_request', 'Review Request'
    REVIEW_FEEDBACK = 'review_feedback', 'Review Feedback'
    BLOCKER = 'blocker', 'Blocker'
    DECISION = 'decision', 'Decision'
    HANDOFF = 'handoff', 'Handoff'
    USER_INPUT = 'user_input', 'User Input'


class AgentMessage(UUIDPrimaryKeyMixin, TimestampMixin):
    """Inter-agent communication"""

    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='agent_messages'
    )

    # Sender/Receiver
    from_agent = models.ForeignKey(
        AgentInstance,
        on_delete=models.CASCADE,
        null=True,  # null = from user
        blank=True,
        related_name='sent_messages'
    )
    to_agent = models.ForeignKey(
        AgentInstance,
        on_delete=models.CASCADE,
        null=True,  # null = broadcast to all
        blank=True,
        related_name='received_messages'
    )

    # Message content
    message_type = models.CharField(
        max_length=20,
        choices=AgentMessageType.choices,
        db_index=True
    )
    content = models.JSONField()
    # Structure varies by type:
    # task_assignment: {"task_id": ..., "instructions": ...}
    # question: {"question": ..., "context": ...}
    # decision: {"decision": ..., "reasoning": ..., "alternatives": [...]}

    # Context references
    context_refs = models.JSONField(default=list, blank=True)
    # List of related entity IDs: ["task:123", "file:models.py", "decision:456"]

    # Threading
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    # Response tracking
    requires_response = models.BooleanField(default=False)
    responded = models.BooleanField(default=False)

    class Meta:
        db_table = 'agent_messages'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['project', 'created_at']),
            models.Index(fields=['from_agent']),
            models.Index(fields=['to_agent']),
            models.Index(fields=['message_type']),
        ]
        verbose_name = 'Agent Message'
        verbose_name_plural = 'Agent Messages'

    def __str__(self):
        from_name = self.from_agent.agent_type.name if self.from_agent else 'User'
        to_name = self.to_agent.agent_type.name if self.to_agent else 'All'
        return f"{from_name} → {to_name}: {self.message_type}"


class AgentAction(UUIDPrimaryKeyMixin, TimestampMixin):
    """Log of all agent actions (event sourcing)"""

    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='agent_actions'
    )
    agent = models.ForeignKey(
        AgentInstance,
        on_delete=models.CASCADE,
        related_name='actions'
    )
    task = models.ForeignKey(
        'tasks.Task',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='actions'
    )

    # Action details
    action_type = models.CharField(max_length=50, db_index=True)
    # Types: file_created, file_modified, file_deleted, decision_made,
    #        task_created, task_completed, agent_hired, error_occurred, etc.

    action_data = models.JSONField()
    # Structure varies by type

    # For rollback
    is_reversible = models.BooleanField(default=True)
    reverse_action = models.JSONField(null=True, blank=True)

    # Status
    status = models.CharField(max_length=20, default='completed')
    # completed, rolled_back, failed

    class Meta:
        db_table = 'agent_actions'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['project', 'created_at']),
            models.Index(fields=['agent']),
            models.Index(fields=['action_type']),
        ]
        verbose_name = 'Agent Action'
        verbose_name_plural = 'Agent Actions'

    def __str__(self):
        return f"{self.agent.agent_type.name}: {self.action_type}"
