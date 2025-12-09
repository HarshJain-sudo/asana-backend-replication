import uuid
from django.db import models
from django.core.exceptions import ValidationError


class Section(models.Model):
    """
    Section model representing a project section.
    """
    gid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=255)
    project = models.ForeignKey(
        'asana_projects.Project',
        on_delete=models.CASCADE,
        related_name='sections'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'asana_sections_section'
        indexes = [
            models.Index(fields=['project']),
        ]
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.name} ({self.project.name})"
