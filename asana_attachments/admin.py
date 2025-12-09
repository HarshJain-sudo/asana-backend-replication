from django.contrib import admin
from asana_attachments.models.attachment import Attachment


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['gid', 'name', 'task', 'mime_type', 'file_size', 'created_by', 'created_at']
    search_fields = ['gid', 'name', 'task__name', 'mime_type', 'created_by__name']
    list_filter = ['mime_type', 'host', 'created_at']
    readonly_fields = ['gid', 'created_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    raw_id_fields = ['task', 'created_by']
    fieldsets = (
        ('Basic Information', {
            'fields': ('gid', 'name', 'task', 'resource_type', 'created_by')
        }),
        ('File Details', {
            'fields': ('mime_type', 'file_size', 'host')
        }),
        ('URLs', {
            'fields': ('download_url', 'view_url')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
