"""
Task Models

Design Decisions:
1. Hierarchical tasks (Epic > Story > Task > Subtask)
2. Dependencies between tasks
3. Detailed tracking of progress
4. Integration with agent assignment
"""

from django.db import models
from core.mixins import UUIDPrimaryKeyMixin, TimestampMixin


class TaskType(models.TextChoices):
    """Task type choices."""
    EPIC = 'epic', 'Epic'
    STORY = 'story', 'Story'
    TASK = 'task', 'Task'
    SUBTASK = 'subtask', 'Subtask'
    BUG = 'bug', 'Bug'
    REVIEW = 'review', 'Review'


class TaskStatus(models.TextChoices):
    """Task status choices."""
    BACKLOG = 'backlog', 'Backlog'
    TODO = 'todo', 'To Do'
    ASSIGNED = 'assigned', 'Assigned'
    IN_PROGRESS = 'in_progress', 'In Progress'
    BLOCKED = 'blocked', 'Blocked'
    IN_REVIEW = 'in_review', 'In Review'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'


class TaskPriority(models.IntegerChoices):
    """Task priority choices."""
    CRITICAL = 1, 'Critical'
    HIGH = 2, 'High'
    MEDIUM = 3, 'Medium'
    LOW = 4, 'Low'


class Task(UUIDPrimaryKeyMixin, TimestampMixin):
    """Task entity"""

    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    # Hierarchy
    parent_task = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subtasks'
    )

    # Basic info
    title = models.CharField(max_length=500, db_index=True)
    description = models.TextField()
    task_type = models.CharField(
        max_length=20,
        choices=TaskType.choices,
        default=TaskType.TASK,
        db_index=True
    )
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.TODO,
        db_index=True
    )
    priority = models.IntegerField(
        choices=TaskPriority.choices,
        default=TaskPriority.MEDIUM,
        db_index=True
    )

    # Requirements and criteria
    requirements = models.JSONField(default=dict, blank=True)
    # Structure:
    # {
    #     "functional": [...],
    #     "technical": [...],
    #     "files_to_modify": [...],
    #     "affected_components": [...]
    # }

    acceptance_criteria = models.JSONField(default=list, blank=True)
    # List of criteria that must be met:
    # ["User can login with email", "JWT token is returned", ...]

    deliverables = models.JSONField(default=list, blank=True)
    # List of expected outputs:
    # ["apps/users/models.py", "apps/users/tests/test_auth.py", ...]

    # Effort tracking
    estimated_effort = models.IntegerField(null=True, blank=True)  # In hours
    actual_effort = models.IntegerField(null=True, blank=True)  # In hours
    iteration_count = models.IntegerField(default=0)

    # Assignment
    assigned_to = models.ForeignKey(
        'agents.AgentInstance',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks'
    )

    # Completion
    completion_summary = models.TextField(blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'tasks'
        ordering = ['priority', '-created_at']
        indexes = [
            models.Index(fields=['project', 'status']),
            models.Index(fields=['assigned_to', 'status']),
            models.Index(fields=['priority', 'created_at']),
        ]
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return f"[{self.task_type.upper()}] {self.title}"

    @property
    def is_completed(self):
        """Check if task is completed."""
        return self.status == TaskStatus.COMPLETED

    @property
    def is_blocked(self):
        """Check if task is blocked."""
        return self.status == TaskStatus.BLOCKED

    def get_progress(self):
        """Calculate task progress percentage."""
        if not self.acceptance_criteria:
            return 0 if self.status != TaskStatus.COMPLETED else 100

        # This would be calculated based on completed criteria
        # For now, simple status-based calculation
        status_progress = {
            TaskStatus.BACKLOG: 0,
            TaskStatus.TODO: 0,
            TaskStatus.ASSIGNED: 10,
            TaskStatus.IN_PROGRESS: 50,
            TaskStatus.BLOCKED: 50,
            TaskStatus.IN_REVIEW: 90,
            TaskStatus.COMPLETED: 100,
            TaskStatus.CANCELLED: 0,
        }
        return status_progress.get(self.status, 0)


class TaskDependency(UUIDPrimaryKeyMixin, TimestampMixin):
    """Dependencies between tasks"""

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='dependencies'
    )
    depends_on = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='dependents'
    )

    dependency_type = models.CharField(
        max_length=50,
        default='blocking',
        choices=[
            ('blocking', 'Blocking'),
            ('related', 'Related'),
            ('triggered_by', 'Triggered By'),
        ]
    )

    class Meta:
        db_table = 'task_dependencies'
        unique_together = ['task', 'depends_on']
        indexes = [
            models.Index(fields=['task']),
            models.Index(fields=['depends_on']),
        ]
        verbose_name = 'Task Dependency'
        verbose_name_plural = 'Task Dependencies'

    def __str__(self):
        return f"{self.task.title} depends on {self.depends_on.title}"


class TaskLog(UUIDPrimaryKeyMixin, TimestampMixin):
    """Task activity log"""

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='logs'
    )
    agent = models.ForeignKey(
        'agents.AgentInstance',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    log_type = models.CharField(
        max_length=20,
        choices=[
            ('comment', 'Comment'),
            ('status_change', 'Status Change'),
            ('assignment', 'Assignment'),
            ('error', 'Error'),
            ('progress', 'Progress Update'),
        ],
        db_index=True
    )
    content = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'task_logs'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['task', 'created_at']),
        ]
        verbose_name = 'Task Log'
        verbose_name_plural = 'Task Logs'

    def __str__(self):
        return f"{self.task.title}: {self.log_type}"
