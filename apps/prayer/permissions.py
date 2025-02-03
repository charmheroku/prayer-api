from rest_framework import permissions

from apps.prayer.models import GroupMembership


class IsGroupMember(permissions.BasePermission):
    """
    Grants access only if the user is a member of
    the group associated with the object.
    """

    def has_object_permission(self, request, view, obj):
        # If the object has an attribute "group", check membership via obj.group.members
        if hasattr(obj, "group"):
            return obj.group.members.filter(id=request.user.id).exists()

        # Otherwise, assume obj itself might be a Group, so check obj.members
        return obj.members.filter(id=request.user.id).exists()


class IsGroupAdmin(permissions.BasePermission):
    """
    Grants access only if the user is ADMIN in
    the group associated with the object.
    """

    def has_object_permission(self, request, view, obj):
        # If the object has an attribute "group" (e.g. a Prayer referencing a Group)...
        if hasattr(obj, "group"):
            return obj.group.groupmembership_set.filter(
                user=request.user, role=GroupMembership.Role.ADMIN
            ).exists()

        # Otherwise, assume obj is the Group itself
        return obj.groupmembership_set.filter(
            user=request.user, role=GroupMembership.Role.ADMIN
        ).exists()
