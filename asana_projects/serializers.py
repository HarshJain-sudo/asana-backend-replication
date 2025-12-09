from rest_framework import serializers
from asana_projects.models.project import Project


class ProjectCreateRequestSerializer(serializers.Serializer):
    """ProjectRequest schema matching API spec"""
    name = serializers.CharField(required=True, max_length=255)
    workspace = serializers.CharField(required=True, max_length=36)  # GID as string
    team = serializers.CharField(required=False, allow_null=True, max_length=36)  # GID as string
    public = serializers.BooleanField(required=False, default=False)
    archived = serializers.BooleanField(required=False, default=False)
    color = serializers.CharField(required=False, allow_null=True, max_length=7)
    notes = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    due_on = serializers.DateField(required=False, allow_null=True)
    start_on = serializers.DateField(required=False, allow_null=True)
    # Create-only fields
    followers = serializers.CharField(required=False, allow_blank=True)  # Comma-separated string
    owner = serializers.CharField(required=False, allow_null=True, max_length=36)


class ProjectSerializer(serializers.ModelSerializer):
    """Legacy serializer - kept for backward compatibility"""
    workspace_gid = serializers.UUIDField(write_only=True, required=True)
    team_gid = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = Project
        fields = ['gid', 'name', 'workspace_gid', 'team_gid', 'public', 
                  'archived', 'color', 'notes', 'due_date', 'start_on', 
                  'created_at', 'updated_at']
        read_only_fields = ['gid', 'created_at', 'updated_at']


class ProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'public', 'archived', 'color', 'notes', 
                  'due_date', 'start_on']
        extra_kwargs = {field: {'required': False} for field in fields}

