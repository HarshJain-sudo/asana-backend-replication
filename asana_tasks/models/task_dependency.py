import uuid
from django.db import models
from django.core.exceptions import ValidationError


class TaskDependency(models.Model):
    """
    Self-referential relationship for task dependencies.
    """
    gid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    predecessor = models.ForeignKey(
        'asana_tasks.Task',
        related_name='successors',
        on_delete=models.CASCADE
    )
    successor = models.ForeignKey(
        'asana_tasks.Task',
        related_name='predecessors',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'asana_tasks_taskdependency'
        unique_together = [['predecessor', 'successor']]

    def clean(self):
        """Validate task dependency."""
        if self.predecessor and self.successor:
            # Check self-reference
            if self.predecessor.gid == self.successor.gid:
                raise ValidationError(
                    'A task cannot depend on itself.'
                )

            # Validate workspace consistency
            if self.predecessor.workspace.gid != \
               self.successor.workspace.gid:
                raise ValidationError(
                    'Both tasks must belong to the same workspace'
                )

            # Check for circular dependencies (basic check)
            # Full circular check would require graph traversal
            # This is a simplified check
            if hasattr(self.successor, 'predecessors'):
                for dep in self.successor.predecessors.all():
                    if dep.predecessor.gid == self.predecessor.gid:
                        raise ValidationError(
                            'Circular dependency detected'
                        )

    def save(self, *args, **kwargs):
        """Override save to run validations."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.predecessor.name} -> {self.successor.name}"

