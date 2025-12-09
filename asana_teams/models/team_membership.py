import uuid
from django.db import models


class TeamMembership(models.Model):
    """
    Many-to-Many relationship between Teams and Users.
    """
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('MEMBER', 'Member'),
    ]

    gid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    team = models.ForeignKey(
        'asana_teams.Team',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        'asana_users.User',
        on_delete=models.CASCADE
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='MEMBER'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'asana_teams_teammembership'
        unique_together = [['team', 'user']]

    def __str__(self):
        return f"{self.user.name} - {self.team.name} ({self.role})"

