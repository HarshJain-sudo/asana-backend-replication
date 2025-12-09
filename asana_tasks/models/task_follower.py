import uuid
from django.db import models


class TaskFollower(models.Model):
    """
    Many-to-Many relationship between Tasks and Users (followers).
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
    user = models.ForeignKey(
        'asana_users.User',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'asana_tasks_taskfollower'
        unique_together = [['task', 'user']]

    def __str__(self):
        return f"{self.user.name} follows {self.task.name}"

