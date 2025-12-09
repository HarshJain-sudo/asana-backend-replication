from rest_framework import serializers
from asana_stories.models.story import Story


class StorySerializer(serializers.ModelSerializer):
    task_gid = serializers.UUIDField(write_only=True, required=True)
    
    class Meta:
        model = Story
        fields = ['gid', 'task_gid', 'text', 'html_text', 'type', 
                  'is_pinned', 'created_at']
        read_only_fields = ['gid', 'created_at', 'type']


class StoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['text', 'html_text', 'is_pinned']
        extra_kwargs = {field: {'required': False} for field in fields}

