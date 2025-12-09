from django.contrib import admin
from asana_projects.models.project import Project, ProjectMember, ProjectFollower


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['gid', 'name', 'workspace', 'team', 'public', 'archived', 'due_on', 'created_at']
    search_fields = ['name', 'gid', 'workspace__name', 'team__name', 'notes']
    list_filter = ['public', 'archived', 'completed', 'workspace', 'team', 'created_at']
    readonly_fields = ['gid', 'created_at', 'modified_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    raw_id_fields = ['workspace', 'team', 'owner', 'created_by', 'completed_by']
    fieldsets = (
        ('Basic Information', {
            'fields': ('gid', 'name', 'workspace', 'team', 'owner', 'created_by')
        }),
        ('Settings', {
            'fields': ('public', 'archived', 'completed', 'color', 'icon', 'default_view')
        }),
        ('Content', {
            'fields': ('notes', 'html_notes')
        }),
        ('Dates', {
            'fields': ('start_on', 'due_on', 'completed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'modified_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ['gid', 'project', 'user', 'access_level', 'created_at']
    search_fields = ['project__name', 'user__name']
    list_filter = ['access_level', 'created_at']
    raw_id_fields = ['project', 'user']


@admin.register(ProjectFollower)
class ProjectFollowerAdmin(admin.ModelAdmin):
    list_display = ['gid', 'project', 'user', 'created_at']
    search_fields = ['project__name', 'user__name']
    list_filter = ['created_at']
    raw_id_fields = ['project', 'user']
