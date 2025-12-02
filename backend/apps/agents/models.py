"""Agent models."""

import uuid
from django.db import models


class Agent(models.Model):
    """AI Agent definitions."""

    AGENT_TYPES = [
        ('backend', 'Backend Developer'),
        ('frontend', 'Frontend Developer'),
        ('devops', 'DevOps Engineer'),
        ('fullstack', 'Full Stack Developer'),
        ('designer', 'UI/UX Designer'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=AGENT_TYPES)
    system_prompt = models.TextField()
    capabilities = models.JSONField(default=list)  # List of capabilities
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'agents_agent'

    def __str__(self):
        return f"{self.name} ({self.type})"


class AgentAssignment(models.Model):
    """Assigns agents to projects."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='agent_assignments'
    )
    agent = models.ForeignKey(
        Agent,
        on_delete=models.CASCADE,
        related_name='project_assignments'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'agents_agentassignment'
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'agent'],
                name='unique_project_agent'
            )
        ]

    def __str__(self):
        return f"{self.agent.name} → {self.project.name}"
