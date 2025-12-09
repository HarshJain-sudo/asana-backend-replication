from rest_framework import serializers
from asana_teams.models.team import Team


class TeamCompactSerializer(serializers.Serializer):
    """TeamCompact schema matching API spec"""
    gid = serializers.CharField()
    resource_type = serializers.CharField(default='team')
    name = serializers.CharField()


class TeamResponseSerializer(serializers.Serializer):
    """TeamResponse schema matching API spec"""
    gid = serializers.CharField()
    resource_type = serializers.CharField(default='team')
    name = serializers.CharField()
    description = serializers.CharField(required=False, allow_null=True)
    workspace = serializers.DictField(required=False)
    created_at = serializers.DateTimeField(required=False)
    modified_at = serializers.DateTimeField(required=False)


class TeamCreateRequestSerializer(serializers.Serializer):
    """TeamRequest schema matching API spec"""
    name = serializers.CharField(required=True, max_length=255)
    workspace = serializers.CharField(required=True, max_length=36)  # GID as string
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)


class TeamUpdateRequestSerializer(serializers.Serializer):
    """TeamUpdateRequest schema matching API spec"""
    name = serializers.CharField(required=False, max_length=255)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)


class TeamAddUserRequestSerializer(serializers.Serializer):
    """TeamAddUserRequest schema matching API spec"""
    user = serializers.CharField(required=True, max_length=36)  # Can be "me", email, or GID


class TeamRemoveUserRequestSerializer(serializers.Serializer):
    """TeamRemoveUserRequest schema matching API spec"""
    user = serializers.CharField(required=True, max_length=36)


class TeamListResponseSerializer(serializers.Serializer):
    """Response for list of teams"""
    data = TeamCompactSerializer(many=True)


class TeamSingleResponseSerializer(serializers.Serializer):
    """Response for single team"""
    data = TeamResponseSerializer()


class ErrorResponseSerializer(serializers.Serializer):
    """Standard error response"""
    errors = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )

