import uuid
from django.db import models
from django.core.exceptions import ValidationError


class UserWorkspaceMembership(models.Model):
    """
    Many-to-Many relationship between Users and Workspaces.
    """
    gid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        'asana_users.User',
        on_delete=models.CASCADE
    )
    workspace = models.ForeignKey(
        'asana_workspaces.Workspace',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'asana_users_userworkspacemembership'
        unique_together = [['user', 'workspace']]

    def __str__(self):
        return f"{self.user.name} - {self.workspace.name}"

