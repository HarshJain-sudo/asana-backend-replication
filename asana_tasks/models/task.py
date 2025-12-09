import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Task(models.Model):
    """
    Task model representing an Asana task.
    """
    ASSIGNEE_STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('later', 'Later'),
        ('new', 'New'),
        ('inbox', 'Inbox'),
        ('today', 'Today'),
    ]

    RESOURCE_SUBTYPE_CHOICES = [
        ('default_task', 'Default Task'),
        ('milestone', 'Milestone'),
        ('approval', 'Approval'),
    ]

    gid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=255)
    resource_subtype = models.CharField(
        max_length=20,
        choices=RESOURCE_SUBTYPE_CHOICES,
        default='default_task'
    )
    workspace = models.ForeignKey(
        'asana_workspaces.Workspace',
        on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='subtasks',
        on_delete=models.CASCADE
    )
    assignee = models.ForeignKey(
        'asana_users.User',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    assignee_status = models.CharField(
        max_length=20,
        choices=ASSIGNEE_STATUS_CHOICES,
        default='inbox'
    )
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    due_on = models.DateField(null=True, blank=True)
    due_at = models.DateTimeField(null=True, blank=True)
    start_on = models.DateField(null=True, blank=True)
    start_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    html_notes = models.TextField(null=True, blank=True)
    num_hearts = models.IntegerField(default=0)
    num_likes = models.IntegerField(default=0)
    num_subtasks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'asana_users.User',
        null=True,
        blank=True,
        related_name='created_tasks',
        on_delete=models.SET_NULL
    )

    class Meta:
        db_table = 'asana_tasks_task'
        indexes = [
            models.Index(fields=['workspace']),
            models.Index(fields=['assignee']),
            models.Index(fields=['completed']),
            models.Index(fields=['due_on']),
            models.Index(fields=['due_at']),
            models.Index(fields=['created_by']),
        ]

    def clean(self):
        """Validate task data."""
        # Auto-set completed_at when completed=True
        if self.completed and not self.completed_at:
            self.completed_at = timezone.now()
        elif not self.completed and self.completed_at:
            self.completed_at = None

        # Validate date ranges
        if self.due_on and self.due_at:
            from datetime import datetime, date
            if isinstance(self.due_at, datetime):
                due_at_date = self.due_at.date()
            else:
                due_at_date = self.due_at
            if due_at_date < self.due_on:
                raise ValidationError(
                    'due_at must be >= due_on'
                )

        if self.start_on and self.start_at:
            from datetime import datetime, date
            if isinstance(self.start_at, datetime):
                start_at_date = self.start_at.date()
            else:
                start_at_date = self.start_at
            if start_at_date < self.start_on:
                raise ValidationError(
                    'start_at must be >= start_on'
                )

    def save(self, *args, **kwargs):
        """Override save to run validations."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

