import uuid
from django.db import models


class Workspace(models.Model):
    """
    Workspace model representing an Asana workspace.
    """
    gid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=255)
    is_organization = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'asana_workspaces_workspace'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['is_organization']),
        ]

    def __str__(self):
        return self.name

