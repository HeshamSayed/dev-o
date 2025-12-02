"""Memory models."""

import uuid
from django.db import models
from django.conf import settings


class UserMemory(models.Model):
    """User memory for AI context."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='memories'
    )
    key = models.CharField(max_length=255)  # e.g., "preferred_language", "user_expertise"
    value = models.TextField()
    category = models.CharField(max_length=100, blank=True)  # e.g., "preferences", "facts", "skills"
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'memory_usermemory'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'key'],
                name='unique_user_memory_key'
            )
        ]

    def __str__(self):
        return f"{self.user.email} - {self.key}"
