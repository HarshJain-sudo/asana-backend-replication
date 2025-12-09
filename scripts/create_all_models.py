#!/usr/bin/env python3
"""
Script to create all missing database models for Asana API implementation.
This script generates model files following the existing Clean Architecture pattern.
"""

import os
import uuid
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Model definitions based on API spec
MODELS = {
    'asana_sections': {
        'section.py': '''import uuid
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
''',
    },
    'asana_project_statuses': {
        'project_status.py': '''import uuid
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
''',
    },
    'asana_project_briefs': {
        'project_brief.py': '''import uuid
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
''',
    },
    'asana_user_task_lists': {
        'user_task_list.py': '''import uuid
from django.db import models


class UserTaskList(models.Model):
    """
    UserTaskList model representing a user's personal task list.
    """
    gid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        'asana_users.User',
        on_delete=models.CASCADE,
        related_name='task_lists'
    )
    workspace = models.ForeignKey(
        'asana_workspaces.Workspace',
        on_delete=models.CASCADE,
        related_name='user_task_lists'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'asana_user_task_lists_usertasklist'
        indexes = [
            models.Index(fields=['owner']),
            models.Index(fields=['workspace']),
        ]
        unique_together = ['owner', 'workspace']
    
    def __str__(self):
        return f"{self.name} ({self.owner.name})"
''',
    },
}

def create_model_file(app_name, model_name, content):
    """Create a model file in the specified app."""
    app_dir = BASE_DIR / app_name / 'models'
    app_dir.mkdir(parents=True, exist_ok=True)
    
    model_file = app_dir / f'{model_name}.py'
    with open(model_file, 'w') as f:
        f.write(content)
    
    # Create __init__.py if it doesn't exist
    init_file = app_dir / '__init__.py'
    if not init_file.exists():
        with open(init_file, 'w') as f:
            f.write(f'from .{model_name} import *\n')

if __name__ == '__main__':
    print("Creating all missing models...")
    for app_name, models_dict in MODELS.items():
        for model_file, content in models_dict.items():
            model_name = model_file.replace('.py', '')
            create_model_file(app_name, model_name, content)
            print(f"✅ Created {app_name}/models/{model_file}")
    print("Done!")

