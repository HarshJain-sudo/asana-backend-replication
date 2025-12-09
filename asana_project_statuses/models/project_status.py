import uuid
from django.db import models


class ProjectStatus(models.Model):
    """
    ProjectStatus model representing a project status update.
    """
    COLOR_CHOICES = [
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('red', 'Red'),
        ('blue', 'Blue'),
    ]
    
    gid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=255)
    color = models.CharField(
        max_length=10,
        choices=COLOR_CHOICES,
        default='green'
    )
    text = models.TextField()
    html_text = models.TextField(null=True, blank=True)
    project = models.ForeignKey(
        'asana_projects.Project',
        on_delete=models.CASCADE,
        related_name='statuses'
    )
    author = models.ForeignKey(
        'asana_users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_project_statuses'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'asana_project_statuses_projectstatus'
        indexes = [
            models.Index(fields=['project']),
            models.Index(fields=['author']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.project.name}"
