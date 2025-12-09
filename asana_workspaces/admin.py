from django.contrib import admin
from asana_workspaces.models.workspace import Workspace


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ['gid', 'name', 'is_organization', 'created_at', 'updated_at']
    search_fields = ['name', 'gid']
    list_filter = ['is_organization', 'created_at']
    readonly_fields = ['gid', 'created_at', 'updated_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
