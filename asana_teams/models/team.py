import uuid
from django.db import models


class Team(models.Model):
    """
    Team model representing an Asana team.
    """
    gid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=255)
    workspace = models.ForeignKey(
        'asana_workspaces.Workspace',
        on_delete=models.CASCADE
    )
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'asana_teams_team'
        indexes = [
            models.Index(fields=['workspace']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name

