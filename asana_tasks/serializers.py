from rest_framework import serializers
from asana_tasks.models.task import Task


class TaskCreateRequestSerializer(serializers.Serializer):
    """TaskRequest schema matching API spec"""
    name = serializers.CharField(required=True, max_length=255)
    workspace = serializers.CharField(required=True, max_length=36)  # GID as string
    assignee = serializers.CharField(required=False, allow_null=True, max_length=36)  # GID as string
    assignee_status = serializers.ChoiceField(
        choices=['upcoming', 'later', 'new', 'inbox', 'today'],
        required=False
    )
    completed = serializers.BooleanField(required=False, default=False)
    due_on = serializers.DateField(required=False, allow_null=True)
    due_at = serializers.DateTimeField(required=False, allow_null=True)
    start_on = serializers.DateField(required=False, allow_null=True)
    start_at = serializers.DateTimeField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    html_notes = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    # Create-only fields (from spec)
    projects = serializers.ListField(
        child=serializers.CharField(max_length=36),
        required=False,
        allow_empty=True
    )
    tags = serializers.ListField(
        child=serializers.CharField(max_length=36),
        required=False,
        allow_empty=True
    )
    followers = serializers.ListField(
        child=serializers.CharField(max_length=36),
        required=False,
        allow_empty=True
    )
    parent = serializers.CharField(required=False, allow_null=True, max_length=36)


class TaskSerializer(serializers.ModelSerializer):
    """Legacy serializer - kept for backward compatibility"""
    workspace_gid = serializers.UUIDField(write_only=True, required=True)
    assignee_gid = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = Task
        fields = ['gid', 'name', 'workspace_gid', 'assignee_gid', 
                  'assignee_status', 'completed', 'due_on', 'due_at', 
                  'start_on', 'start_at', 'notes', 'html_notes',
                  'created_at', 'updated_at']
        read_only_fields = ['gid', 'completed_at', 'created_at', 'updated_at']


class TaskUpdateSerializer(serializers.ModelSerializer):
    assignee_gid = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = Task
        fields = ['name', 'assignee_gid', 'assignee_status', 'completed', 
                  'due_on', 'due_at', 'start_on', 'start_at', 'notes', 'html_notes']
        extra_kwargs = {field: {'required': False} for field in fields}


class TaskProjectSerializer(serializers.Serializer):
    project_gid = serializers.UUIDField(required=True)


class TaskTagSerializer(serializers.Serializer):
    tag_gid = serializers.UUIDField(required=True)


class TaskFollowerSerializer(serializers.Serializer):
    followers = serializers.ListField(
        child=serializers.UUIDField(),
        required=True
    )


class TaskDependencySerializer(serializers.Serializer):
    dependencies = serializers.ListField(
        child=serializers.UUIDField(),
        required=True
    )


# Response Serializers (for API spec documentation)

class WorkspaceCompactSerializer(serializers.Serializer):
    """WorkspaceCompact schema matching API spec"""
    gid = serializers.CharField()  # String, not UUID
    resource_type = serializers.CharField(default='workspace')
    name = serializers.CharField()


class UserCompactSerializer(serializers.Serializer):
    """UserCompact schema matching API spec"""
    gid = serializers.CharField()  # String, not UUID
    resource_type = serializers.CharField(default='user')
    name = serializers.CharField()


class ProjectCompactSerializer(serializers.Serializer):
    """ProjectCompact schema matching API spec"""
    gid = serializers.CharField()
    resource_type = serializers.CharField(default='project')
    name = serializers.CharField()


class TagCompactSerializer(serializers.Serializer):
    """TagCompact schema matching API spec"""
    gid = serializers.CharField()
    resource_type = serializers.CharField(default='tag')
    name = serializers.CharField()


# Legacy aliases for backward compatibility
WorkspaceNestedSerializer = WorkspaceCompactSerializer
UserNestedSerializer = UserCompactSerializer


class TaskCompactSerializer(serializers.Serializer):
    """TaskCompact schema matching API spec"""
    gid = serializers.CharField()  # String, not UUID
    resource_type = serializers.CharField(default='task')
    name = serializers.CharField()
    resource_subtype = serializers.CharField(required=False, allow_null=True)


class TaskResponseSerializer(serializers.Serializer):
    """TaskResponse schema matching API spec - extends TaskBase"""
    gid = serializers.CharField()  # String, not UUID
    resource_type = serializers.CharField(default='task')
    name = serializers.CharField()
    resource_subtype = serializers.CharField(required=False, allow_null=True)
    workspace = WorkspaceCompactSerializer()
    assignee = UserCompactSerializer(allow_null=True)
    assignee_status = serializers.CharField(allow_null=True, required=False)
    completed = serializers.BooleanField()
    completed_at = serializers.DateTimeField(allow_null=True, required=False)
    due_on = serializers.DateField(allow_null=True, required=False)
    due_at = serializers.DateTimeField(allow_null=True, required=False)
    start_on = serializers.DateField(allow_null=True, required=False)
    start_at = serializers.DateTimeField(allow_null=True, required=False)
    notes = serializers.CharField(allow_null=True, required=False)
    html_notes = serializers.CharField(allow_null=True, required=False)
    num_hearts = serializers.IntegerField(required=False, default=0)
    num_likes = serializers.IntegerField(required=False, default=0)
    created_at = serializers.DateTimeField()
    modified_at = serializers.DateTimeField()  # Note: spec uses modified_at, not updated_at
    # Nested arrays (from spec)
    projects = ProjectCompactSerializer(many=True, required=False, allow_null=True)
    tags = TagCompactSerializer(many=True, required=False, allow_null=True)
    followers = UserCompactSerializer(many=True, required=False, allow_null=True)


class TaskListResponseSerializer(serializers.Serializer):
    """Response for list of tasks"""
    data = TaskResponseSerializer(many=True)


class TaskSingleResponseSerializer(serializers.Serializer):
    """Response for single task"""
    data = TaskResponseSerializer()


class ErrorMessageSerializer(serializers.Serializer):
    """Error message object"""
    message = serializers.CharField()


class ErrorResponseSerializer(serializers.Serializer):
    """Standard error response"""
    errors = ErrorMessageSerializer(many=True)

