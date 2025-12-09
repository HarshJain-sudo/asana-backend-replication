import uuid
from django.db import models


class UserTaskList(models.Model):
    """
    UserTaskList model representing a user's personal task list.
    """
    gid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        'asana_users.User',
        on_delete=models.CASCADE,
        related_name='task_lists'
    )
    workspace = models.ForeignKey(
        'asana_workspaces.Workspace',
        on_delete=models.CASCADE,
        related_name='user_task_lists'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'asana_user_task_lists_usertasklist'
        indexes = [
            models.Index(fields=['owner']),
            models.Index(fields=['workspace']),
        ]
        unique_together = ['owner', 'workspace']
    
    def __str__(self):
        return f"{self.name} ({self.owner.name})"
