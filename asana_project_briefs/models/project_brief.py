import uuid
from django.db import models


class ProjectBrief(models.Model):
    """
    ProjectBrief model representing a project brief.
    """
    gid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    html_text = models.TextField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    project = models.OneToOneField(
        'asana_projects.Project',
        on_delete=models.CASCADE,
        related_name='brief'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'asana_project_briefs_projectbrief'
    
    def __str__(self):
        return f"Brief for {self.project.name}"
