from rest_framework import serializers
from asana_users.models.user import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['gid', 'name', 'email', 'photo', 'created_at', 'updated_at']
        read_only_fields = ['gid', 'created_at', 'updated_at']


class UserListResponseSerializer(serializers.Serializer):
    data = UserSerializer(many=True)


class UserSingleResponseSerializer(serializers.Serializer):
    data = UserSerializer()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'photo']
        extra_kwargs = {
            'photo': {'required': False},
        }


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'photo']
        extra_kwargs = {
            'name': {'required': False},
            'email': {'required': False},
            'photo': {'required': False},
        }


class ErrorResponseSerializer(serializers.Serializer):
    errors = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )


