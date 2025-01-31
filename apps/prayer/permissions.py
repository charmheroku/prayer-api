from rest_framework import permissions


class IsGroupMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "group"):
            return obj.group.members.filter(id=request.user.id).exists()
        return obj.members.filter(id=request.user.id).exists()


class IsGroupAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "group"):
            return obj.group.groupmembership_set.filter(
                user=request.user, role=GroupMembership.Role.ADMIN
            ).exists()
        return obj.groupmembership_set.filter(
            user=request.user, role=GroupMembership.Role.ADMIN
        ).exists()
