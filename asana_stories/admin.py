from django.contrib import admin
from asana_stories.models.story import Story


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['gid', 'task', 'type', 'is_pinned', 'created_by', 'created_at']
    search_fields = ['gid', 'task__name', 'text', 'created_by__name']
    list_filter = ['type', 'is_pinned', 'created_at']
    readonly_fields = ['gid', 'created_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    raw_id_fields = ['task', 'created_by']
    fieldsets = (
        ('Basic Information', {
            'fields': ('gid', 'task', 'type', 'created_by')
        }),
        ('Content', {
            'fields': ('text', 'html_text', 'is_pinned')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
