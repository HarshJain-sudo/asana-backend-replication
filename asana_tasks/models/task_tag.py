import uuid
from django.db import models
from django.core.exceptions import ValidationError


class TaskTag(models.Model):
    """
    Many-to-Many relationship between Tasks and Tags.
    """
    gid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    task = models.ForeignKey(
        'asana_tasks.Task',
        on_delete=models.CASCADE
    )
    tag = models.ForeignKey(
        'asana_tags.Tag',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'asana_tasks_tasktag'
        unique_together = [['task', 'tag']]

    def clean(self):
        """Validate task-tag relationship."""
        if self.task and self.tag:
            # Validate workspace consistency
            if self.task.workspace.gid != self.tag.workspace.gid:
                raise ValidationError(
                    'Task and Tag must belong to the same workspace'
                )

    def save(self, *args, **kwargs):
        """Override save to run validations."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.task.name} - {self.tag.name}"

