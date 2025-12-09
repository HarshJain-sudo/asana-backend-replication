from django.contrib import admin
from asana_webhooks.models.webhook import Webhook


@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    list_display = ['gid', 'resource', 'resource_gid', 'target', 'active', 'created_at']
    search_fields = ['gid', 'resource', 'resource_gid', 'target']
    list_filter = ['resource', 'active', 'created_at']
    readonly_fields = ['gid', 'created_at', 'updated_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Basic Information', {
            'fields': ('gid', 'resource', 'resource_gid', 'active')
        }),
        ('Webhook Configuration', {
            'fields': ('target', 'secret')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
