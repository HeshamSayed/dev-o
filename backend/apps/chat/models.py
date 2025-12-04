"""Chat models."""

import uuid
from django.db import models
from django.conf import settings


class Conversation(models.Model):
    """Chat conversation - can be normal chat or project chat."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conversations'
    )
    title = models.CharField(max_length=255, blank=True)

    # Link to project if this is a project conversation
    is_project_chat = models.BooleanField(default=False)
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='conversations'
    )

    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'chat_conversation'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user', '-updated_at']),
            models.Index(fields=['user', 'is_project_chat']),
        ]

    def __str__(self):
        return f"{self.title or 'Untitled'} - {self.user.email}"


class Message(models.Model):
    """Chat message."""

    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
        ('agent', 'Agent'),  # For project mode - specific agent
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()

    # Agent name for project mode (CrewAI agents)
    agent_name = models.CharField(max_length=100, blank=True, null=True)

    # AI thinking (shown if user enables it)
    thinking = models.TextField(blank=True, null=True)

    # Files created/modified by this message
    files_affected = models.JSONField(default=list, blank=True)

    token_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chat_message'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation', 'created_at']),
        ]

    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."
