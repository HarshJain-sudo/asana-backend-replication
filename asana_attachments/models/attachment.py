import uuid
from django.db import models


class Attachment(models.Model):
    """
    Attachment model representing file attachments on tasks.
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
    name = models.CharField(max_length=255)
    resource_type = models.CharField(
        max_length=50,
        default='attachment'
    )
    download_url = models.URLField()
    view_url = models.URLField(null=True, blank=True)
    host = models.CharField(max_length=255, null=True, blank=True)
    file_size = models.BigIntegerField(null=True, blank=True)
    mime_type = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        'asana_users.User',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        db_table = 'asana_attachments_attachment'
        indexes = [
            models.Index(fields=['task']),
            models.Index(fields=['created_by']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.name

