from django.contrib import admin
from asana_tags.models.tag import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['gid', 'name', 'workspace', 'color', 'created_at', 'updated_at']
    search_fields = ['name', 'gid', 'workspace__name']
    list_filter = ['workspace', 'created_at']
    readonly_fields = ['gid', 'created_at', 'updated_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    raw_id_fields = ['workspace']
