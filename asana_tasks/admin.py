from django.contrib import admin
from asana_tasks.models.task import Task
from asana_tasks.models.task_project import TaskProject
from asana_tasks.models.task_tag import TaskTag
from asana_tasks.models.task_dependency import TaskDependency
from asana_tasks.models.task_follower import TaskFollower


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['gid', 'name', 'workspace', 'assignee', 'completed', 'due_on', 'created_at']
    search_fields = ['name', 'gid', 'workspace__name', 'assignee__name', 'notes']
    list_filter = ['completed', 'assignee_status', 'workspace', 'created_at', 'due_on']
    readonly_fields = ['gid', 'created_at', 'updated_at', 'completed_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    raw_id_fields = ['workspace', 'assignee', 'created_by']
    fieldsets = (
        ('Basic Information', {
            'fields': ('gid', 'name', 'workspace', 'assignee', 'assignee_status', 'created_by')
        }),
        ('Status', {
            'fields': ('completed', 'completed_at')
        }),
        ('Content', {
            'fields': ('notes', 'html_notes')
        }),
        ('Dates', {
            'fields': ('start_on', 'start_at', 'due_on', 'due_at')
        }),
        ('Engagement', {
            'fields': ('num_hearts', 'num_likes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TaskProject)
class TaskProjectAdmin(admin.ModelAdmin):
    list_display = ['gid', 'task', 'project', 'created_at']
    search_fields = ['task__name', 'project__name', 'gid']
    list_filter = ['created_at']
    readonly_fields = ['gid', 'created_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    raw_id_fields = ['task', 'project']


@admin.register(TaskTag)
class TaskTagAdmin(admin.ModelAdmin):
    list_display = ['gid', 'task', 'tag', 'created_at']
    search_fields = ['task__name', 'tag__name', 'gid']
    list_filter = ['created_at']
    readonly_fields = ['gid', 'created_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    raw_id_fields = ['task', 'tag']


@admin.register(TaskDependency)
class TaskDependencyAdmin(admin.ModelAdmin):
    list_display = ['gid', 'predecessor', 'successor', 'created_at']
    search_fields = ['predecessor__name', 'successor__name', 'gid']
    list_filter = ['created_at']
    readonly_fields = ['gid', 'created_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    raw_id_fields = ['predecessor', 'successor']


@admin.register(TaskFollower)
class TaskFollowerAdmin(admin.ModelAdmin):
    list_display = ['gid', 'task', 'user', 'created_at']
    search_fields = ['task__name', 'user__name', 'user__email', 'gid']
    list_filter = ['created_at']
    readonly_fields = ['gid', 'created_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    raw_id_fields = ['task', 'user']
