import uuid
from django.db import models


class Story(models.Model):
    """
    Story model representing comments/activity on tasks.
    """
    TYPE_CHOICES = [
        ('comment', 'Comment'),
        ('system', 'System'),
    ]

    gid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    task = models.ForeignKey(
        'asana_tasks.Task',
        on_delete=models.CASCADE
    )
    text = models.TextField()
    html_text = models.TextField(null=True, blank=True)
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='comment'
    )
    is_pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        'asana_users.User',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        db_table = 'asana_stories_story'
        indexes = [
            models.Index(fields=['task']),
            models.Index(fields=['created_by']),
            models.Index(fields=['created_at']),
            models.Index(fields=['type']),
        ]

    def __str__(self):
        return f"Story for {self.task.name}"

