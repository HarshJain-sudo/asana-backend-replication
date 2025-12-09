from django.contrib import admin
from asana_users.models.user import User
from asana_users.models.user_workspace_membership import UserWorkspaceMembership


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['gid', 'name', 'email', 'created_at', 'updated_at']
    search_fields = ['name', 'email', 'gid']
    list_filter = ['created_at']
    readonly_fields = ['gid', 'created_at', 'updated_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


@admin.register(UserWorkspaceMembership)
class UserWorkspaceMembershipAdmin(admin.ModelAdmin):
    list_display = ['gid', 'user', 'workspace', 'created_at']
    search_fields = ['user__name', 'user__email', 'workspace__name', 'gid']
    list_filter = ['created_at']
    readonly_fields = ['gid', 'created_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    raw_id_fields = ['user', 'workspace']
