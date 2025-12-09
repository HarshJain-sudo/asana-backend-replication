from rest_framework import serializers
from asana_tags.models.tag import Tag
from asana_backend.utils.validators import validate_hex_color
from django.core.exceptions import ValidationError


class TagCompactSerializer(serializers.Serializer):
    """TagCompact schema matching API spec"""
    gid = serializers.CharField()
    resource_type = serializers.CharField(default='tag')
    name = serializers.CharField()


class TagResponseSerializer(serializers.Serializer):
    """TagResponse schema matching API spec"""
    gid = serializers.CharField()
    resource_type = serializers.CharField(default='tag')
    name = serializers.CharField()
    color = serializers.CharField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(required=False)
    workspace = serializers.DictField(required=False)
    followers = serializers.ListField(
        child=serializers.DictField(),
        required=False
    )
    permalink_url = serializers.URLField(required=False)


class TagCreateRequestSerializer(serializers.Serializer):
    """TagCreateRequest schema matching API spec"""
    name = serializers.CharField(required=True, max_length=255)
    workspace = serializers.CharField(required=True, max_length=36)  # GID as string
    color = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=7)
    notes = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    followers = serializers.ListField(
        child=serializers.CharField(max_length=255),
        required=False
    )
    
    def validate_color(self, value):
        if value:
            try:
                return validate_hex_color(value)
            except ValidationError as e:
                raise serializers.ValidationError(str(e))
        return value


class TagUpdateRequestSerializer(serializers.Serializer):
    """TagUpdateRequest schema matching API spec"""
    name = serializers.CharField(required=False, max_length=255)
    color = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=7)
    notes = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    
    def validate_color(self, value):
        if value:
            try:
                return validate_hex_color(value)
            except ValidationError as e:
                raise serializers.ValidationError(str(e))
        return value


class TagCreateTagForWorkspaceRequestSerializer(serializers.Serializer):
    """TagCreateTagForWorkspaceRequest schema matching API spec"""
    name = serializers.CharField(required=True, max_length=255)
    color = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=7)
    notes = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    followers = serializers.ListField(
        child=serializers.CharField(max_length=255),
        required=False
    )
    
    def validate_color(self, value):
        if value:
            try:
                return validate_hex_color(value)
            except ValidationError as e:
                raise serializers.ValidationError(str(e))
        return value


class TagListResponseSerializer(serializers.Serializer):
    """Response for list of tags"""
    data = TagCompactSerializer(many=True)
    next_page = serializers.DictField(
        child=serializers.CharField(),
        allow_null=True,
        required=False
    )


class TagSingleResponseSerializer(serializers.Serializer):
    """Response for single tag"""
    data = TagResponseSerializer()


class ErrorResponseSerializer(serializers.Serializer):
    """Standard error response"""
    errors = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )

