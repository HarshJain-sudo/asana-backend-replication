import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Project(models.Model):
    """
    Project model representing an Asana project.
    Matches Asana API ProjectResponse schema from api_spec.txt
    """
    
    # Layout choices (default_view)
    LAYOUT_CHOICES = [
        ('list', 'List'),
        ('board', 'Board'),
        ('calendar', 'Calendar'),
        ('timeline', 'Timeline'),
    ]
    
    # Icon choices
    ICON_CHOICES = [
        ('list', 'list'),
        ('board',
         'board'),
        ('timeline', 'timeline'),
        ('calendar', 'calendar'),
        ('rocket', 'rocket'),
        ('people', 'people'),
        ('graph', 'graph'),
        ('star', 'star'),
        ('bug', 'bug'),
        ('light_bulb', 'light_bulb'),
        ('globe', 'globe'),
        ('gear', 'gear'),
        ('notebook', 'notebook'),
        ('computer', 'computer'),
        ('check', 'check'),
        ('target', 'target'),
        ('html', 'html'),
        ('megaphone', 'megaphone'),
        ('chat_bubbles', 'chat_bubbles'),
        ('briefcase', 'briefcase'),
        ('page_layout', 'page_layout'),
        ('mountain_flag', 'mountain_flag'),
        ('puzzle', 'puzzle'),
        ('presentation', 'presentation'),
        ('line_and_symbols', 'line_and_symbols'),
        ('speed_dial', 'speed_dial'),
        ('ribbon', 'ribbon'),
        ('shoe', 'shoe'),
        ('shopping_basket', 'shopping_basket'),
        ('map', 'map'),
        ('ticket', 'ticket'),
        ('coins', 'coins'),
    ]
    
    # Color choices
    COLOR_CHOICES = [
        ('dark-pink', 'Dark Pink'),
        ('dark-green', 'Dark Green'),
        ('dark-blue', 'Dark Blue'),
        ('dark-red', 'Dark Red'),
        ('dark-teal', 'Dark Teal'),
        ('dark-brown', 'Dark Brown'),
        ('dark-orange', 'Dark Orange'),
        ('dark-purple', 'Dark Purple'),
        ('dark-warm-gray', 'Dark Warm Gray'),
        ('light-pink', 'Light Pink'),
        ('light-green', 'Light Green'),
        ('light-blue', 'Light Blue'),
        ('light-red', 'Light Red'),
        ('light-teal', 'Light Teal'),
        ('light-brown', 'Light Brown'),
        ('light-orange', 'Light Orange'),
        ('light-purple', 'Light Purple'),
        ('light-warm-gray', 'Light Warm Gray'),
        ('none', 'None'),
    ]
    
    gid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=255)
    workspace = models.ForeignKey(
        'asana_workspaces.Workspace',
        on_delete=models.CASCADE,
        related_name='projects'
    )
    team = models.ForeignKey(
        'asana_teams.Team',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='projects'
    )
    owner = models.ForeignKey(
        'asana_users.User',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='owned_projects'
    )
    
    # Status fields
    public = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    completed_by = models.ForeignKey(
        'asana_users.User',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='completed_projects'
    )
    
    # Appearance
    color = models.CharField(
        max_length=20,
        choices=COLOR_CHOICES,
        null=True,
        blank=True
    )
    icon = models.CharField(
        max_length=30,
        choices=ICON_CHOICES,
        null=True,
        blank=True
    )
    default_view = models.CharField(
        max_length=20,
        choices=LAYOUT_CHOICES,
        default='list'
    )
    
    # Content
    notes = models.TextField(null=True, blank=True)
    html_notes = models.TextField(null=True, blank=True)
    
    # Dates
    due_on = models.DateField(null=True, blank=True)
    start_on = models.DateField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    # Relationships
    created_by = models.ForeignKey(
        'asana_users.User',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='created_projects'
    )

    class Meta:
        db_table = 'asana_projects_project'
        indexes = [
            models.Index(fields=['workspace']),
            models.Index(fields=['team']),
            models.Index(fields=['archived']),
            models.Index(fields=['public']),
            models.Index(fields=['completed']),
            models.Index(fields=['owner']),
        ]

    def clean(self):
        """Validate project data."""
        # Auto-set completed_at when completed=True
        if self.completed and not self.completed_at:
            self.completed_at = timezone.now()
        elif not self.completed:
            self.completed_at = None
            self.completed_by = None

        # Validate date range
        if self.due_on and self.start_on:
            if self.due_on < self.start_on:
                raise ValidationError('due_on must be >= start_on')

        # Validate team belongs to same workspace
        if self.team and self.workspace:
            if self.team.workspace.gid != self.workspace.gid:
                raise ValidationError('Team must belong to the same workspace')

    def save(self, *args, **kwargs):
        """Override save to run validations."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProjectMember(models.Model):
    """
    Project member relationship (many-to-many between Project and User).
    """
    ACCESS_LEVEL_CHOICES = [
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('commenter', 'Commenter'),
        ('viewer', 'Viewer'),
    ]
    
    gid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='members'
    )
    user = models.ForeignKey(
        'asana_users.User',
        on_delete=models.CASCADE,
        related_name='project_memberships'
    )
    access_level = models.CharField(
        max_length=20,
        choices=ACCESS_LEVEL_CHOICES,
        default='editor'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'asana_projects_project_member'
        unique_together = ['project', 'user']


class ProjectFollower(models.Model):
    """
    Project follower relationship.
    """
    gid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    user = models.ForeignKey(
        'asana_users.User',
        on_delete=models.CASCADE,
        related_name='followed_projects'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'asana_projects_project_follower'
        unique_together = ['project', 'user']
