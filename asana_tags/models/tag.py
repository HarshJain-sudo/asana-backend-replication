import uuid
from django.db import models
from django.core.exceptions import ValidationError
from asana_backend.utils.validators import validate_hex_color


class Tag(models.Model):
    """
    Tag model representing an Asana tag.
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
    color = models.CharField(max_length=7, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'asana_tags_tag'
        indexes = [
            models.Index(fields=['workspace']),
            models.Index(fields=['name']),
        ]
        unique_together = [['workspace', 'name']]

    def clean(self):
        """Validate tag data."""
        # Validate color format
        if self.color:
            try:
                self.color = validate_hex_color(self.color)
            except ValidationError as e:
                raise ValidationError({'color': str(e)})

    def save(self, *args, **kwargs):
        """Override save to run validations."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

