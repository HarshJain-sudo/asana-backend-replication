import uuid
from django.db import models
from django.core.exceptions import ValidationError


class TaskProject(models.Model):
    """
    Many-to-Many relationship between Tasks and Projects.
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
    project = models.ForeignKey(
        'asana_projects.Project',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'asana_tasks_taskproject'
        unique_together = [['task', 'project']]

    def clean(self):
        """Validate task-project relationship."""
        if self.task and self.project:
            # Validate workspace consistency
            if self.task.workspace.gid != self.project.workspace.gid:
                raise ValidationError(
                    'Task and Project must belong to the same workspace'
                )

    def save(self, *args, **kwargs):
        """Override save to run validations."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.task.name} - {self.project.name}"

