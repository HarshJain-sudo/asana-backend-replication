from django.contrib import admin
from asana_teams.models.team import Team
from asana_teams.models.team_membership import TeamMembership


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['gid', 'name', 'workspace', 'created_at', 'updated_at']
    search_fields = ['name', 'gid', 'workspace__name', 'description']
    list_filter = ['workspace', 'created_at']
    readonly_fields = ['gid', 'created_at', 'updated_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    raw_id_fields = ['workspace']


@admin.register(TeamMembership)
class TeamMembershipAdmin(admin.ModelAdmin):
    list_display = ['gid', 'team', 'user', 'role', 'created_at']
    search_fields = ['team__name', 'user__name', 'user__email', 'gid']
    list_filter = ['role', 'created_at']
    readonly_fields = ['gid', 'created_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    raw_id_fields = ['team', 'user']
