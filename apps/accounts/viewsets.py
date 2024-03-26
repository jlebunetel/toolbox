"""Viewsets definitions for the 'accounts' application."""

from accounts.models import User
from accounts.serializers import GroupSerializer, PermissionSerializer, UserSerializer
from django.contrib.auth.models import Group, Permission
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ReadOnlyModelViewSet


class PermissionViewset(ReadOnlyModelViewSet):  # pylint: disable=too-many-ancestors
    """Viewset definition for 'Permission' model."""

    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAdminUser]


class GroupViewset(ReadOnlyModelViewSet):  # pylint: disable=too-many-ancestors
    """Viewset definition for 'Group' model."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]


class UserViewset(ReadOnlyModelViewSet):  # pylint: disable=too-many-ancestors
    """Viewset definition for 'User' model."""

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
