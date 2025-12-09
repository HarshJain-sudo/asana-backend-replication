import uuid
from django.db import models


class User(models.Model):
    """
    User model representing an Asana user.
    """
    gid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    photo = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'asana_users_user'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name

