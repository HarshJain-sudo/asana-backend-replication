import uuid
from django.db import models
from django.core.exceptions import ValidationError
from asana_backend.utils.validators import validate_uuid


class Webhook(models.Model):
    RESOURCE_TYPES = [
        'task',
        'project',
        'workspace',
        'team',
        'tag',
        'story',
        'attachment',
    ]
    """
    Webhook model for event notifications.
    """
    gid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    resource = models.CharField(max_length=50)
    resource_gid = models.CharField(max_length=36)
    target = models.URLField()
    active = models.BooleanField(default=True)
    secret = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'asana_webhooks_webhook'
        indexes = [
            models.Index(fields=['resource']),
            models.Index(fields=['resource_gid']),
            models.Index(fields=['active']),
        ]

    def clean(self):
        """Validate webhook data."""
        # Validate resource type
        if self.resource and self.resource not in self.RESOURCE_TYPES:
            raise ValidationError(
                f'Resource type must be one of: {", ".join(self.RESOURCE_TYPES)}'
            )

        # Validate resource_gid is valid UUID
        if self.resource_gid:
            try:
                validate_uuid(self.resource_gid)
            except ValidationError as e:
                raise ValidationError(
                    {'resource_gid': str(e)}
                )

    def save(self, *args, **kwargs):
        """Override save to run validations."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Webhook for {self.resource} {self.resource_gid}"

