from rest_framework import serializers
from asana_workspaces.models.workspace import Workspace


class WorkspaceSerializer(serializers.ModelSerializer):
    email_domains = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_null=True,
        default=list
    )
    
    class Meta:
        model = Workspace
        fields = ['gid', 'resource_type', 'name', 'is_organization', 'email_domains', 'created_at', 'updated_at']
        read_only_fields = ['gid', 'resource_type', 'created_at', 'updated_at']


class WorkspaceListResponseSerializer(serializers.Serializer):
    data = WorkspaceSerializer(many=True)


class WorkspaceSingleResponseSerializer(serializers.Serializer):
    data = WorkspaceSerializer()


class WorkspaceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ['name', 'is_organization']


class WorkspaceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ['name', 'is_organization']
        extra_kwargs = {
            'name': {'required': False},
            'is_organization': {'required': False},
        }


class WorkspaceAddUserRequestSerializer(serializers.Serializer):
    """WorkspaceAddUserRequest schema matching API spec"""
    user = serializers.CharField(required=True, max_length=255)  # Can be "me", email, or GID


class WorkspaceRemoveUserRequestSerializer(serializers.Serializer):
    """WorkspaceRemoveUserRequest schema matching API spec"""
    user = serializers.CharField(required=True, max_length=255)  # Can be "me", email, or GID


class ErrorResponseSerializer(serializers.Serializer):
    errors = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )

