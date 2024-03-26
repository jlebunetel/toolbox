"""Serializers definitions for the 'accounts' application."""

from accounts.models import User
from django.contrib.auth.models import Group, Permission
from rest_framework import serializers


class PermissionSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer definition for 'Permission' model."""

    class Meta:
        """Metadata options class."""

        model = Permission
        exclude = [
            "content_type",
        ]
        extra_kwargs = {
            "url": {
                "view_name": "accounts_api:permissions-detail",
                "lookup_field": "pk",
            },
        }


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer definition for 'Group' model."""

    class Meta:
        """Metadata options class."""

        model = Group
        fields = [
            "url",
            "name",
            "permissions",
            "user_set",
        ]
        extra_kwargs = {
            "url": {
                "view_name": "accounts_api:groups-detail",
                "lookup_field": "pk",
            },
            "permissions": {
                "view_name": "accounts_api:permissions-detail",
                "lookup_field": "pk",
            },
            "user_set": {
                "view_name": "accounts_api:users-detail",
                "lookup_field": "pk",
            },
        }


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer definition for 'User' model."""

    class Meta:
        """Metadata options class."""

        model = User
        fields = [
            "url",
            "username",
            "first_name",
            "last_name",
        ]
        extra_kwargs = {
            "url": {
                "view_name": "accounts_api:users-detail",
                "lookup_field": "pk",
            },
        }
