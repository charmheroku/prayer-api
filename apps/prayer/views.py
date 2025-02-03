from django.shortcuts import render  # noqa: F401
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import (
    Prayer,
    PrayerCategory,
    Group,
    GroupMembership,
    MembershipRequest,
)
from apps.prayer.serializers import (
    PrayerSerializer,
    PrayerCategorySerializer,
    GroupSerializer,
    MembershipRequestSerializer,
)
from .permissions import IsGroupAdmin


class PrayerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Prayer objects.
    """

    serializer_class = PrayerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        """
        Object-level permission is used here.
        We dynamically return different permission classes
        depending on the action.
        """
        if self.action in ["update", "partial_update", "destroy"]:
            # Only the group admin or the author can change or remove prayers
            # We'll check group-admin with IsGroupAdmin, and check the author in the method has_object_permission or override
            return [permissions.IsAuthenticated(), IsGroupAdmin()]
        else:
            # For create, retrieve, list - at least be authenticated
            return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """
        Returns a filtered queryset:
        1) public prayers are visible to everyone (authenticated),
        2) private prayers only to the author,
        3) group-level prayers only to group members.
        """
        user = self.request.user
        return Prayer.objects.filter(
            Q(privacy_level=Prayer.PrivacyLevel.PUBLIC)
            | Q(author=user)
            | Q(privacy_level=Prayer.PrivacyLevel.GROUP, group__members=user)
        ).distinct()

    def perform_create(self, serializer):
        """
        Automatically assign the author to the prayer upon creation.
        """
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"])
    def pray(self, request, pk=None):
        """
        A custom action to increment the 'prayer_count'
        when a user prays for this particular request.
        """
        prayer = self.get_object()
        prayer.prayer_count += 1
        prayer.save()
        return Response({"status": "prayer counted"})


class PrayerCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for PrayerCategory model.
    """

    queryset = PrayerCategory.objects.all()
    serializer_class = PrayerCategorySerializer

    def get_permissions(self):
        """
        Only site administrators can create/update/delete categories.
        Any user can read them.
        """
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class GroupViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Group model.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        """
        If the user wants to update or destroy a group,
        they must be the group admin (IsGroupAdmin).
        For creation, any authenticated user is allowed.
        For read operations, any authenticated user can view,
        but we also filter the queryset in get_queryset.
        """
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsGroupAdmin()]
        elif self.action == "create":
            return [permissions.IsAuthenticated()]
        else:
            # For list and retrieve
            return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """
        Returns:
        1) public groups (is_private=False)
        2) private groups if the user is a member
        """
        user = self.request.user
        return Group.objects.filter(
            Q(is_private=False) | Q(members=user)
        ).distinct()

    def perform_create(self, serializer):
        """
        Upon group creation, the creator is automatically assigned as ADMIN.
        """
        group = serializer.save(created_by=self.request.user)
        GroupMembership.objects.create(
            user=self.request.user,
            group=group,
            role=GroupMembership.Role.ADMIN,
        )

    @action(detail=True, methods=["post"])
    def join(self, request, pk=None):
        """
        Directly join the group if it's public (is_private=False).
        If it's a private group, return a message to send a request-join.
        """
        group = self.get_object()
        if group.members.filter(id=request.user.id).exists():
            return Response(
                {"detail": "You are already a member of this group"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Private groups cannot be joined directly
        if group.is_private:
            return Response(
                {"detail": "This group is private. Please request to join."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Create GroupMembership
        GroupMembership.objects.create(
            user=request.user, group=group, role=GroupMembership.Role.MEMBER
        )
        return Response(
            {"detail": "Successfully joined the group"},
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["post"], url_path="request-join")
    def request_join(self, request, pk=None):
        """
        For private groups, users must send a membership request.
        """
        try:
            # Important: here we use Group.objects.get instead of self.get_object()
            group = Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            return Response(
                {"detail": "Group not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if group.members.filter(id=request.user.id).exists():
            return Response(
                {"detail": "You are already in this group"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not group.is_private:
            return Response(
                {
                    "detail": "This group is not private. You can directly join."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check for duplicate pending request
        existing_req = MembershipRequest.objects.filter(
            group=group,
            user=request.user,
            status=MembershipRequest.Status.PENDING,
        ).first()
        if existing_req:
            return Response(
                {"detail": "You already have a pending request"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create new membership request
        reason = request.data.get("reason", "")
        membership_request = MembershipRequest.objects.create(
            group=group, user=request.user, reason=reason
        )
        serializer = MembershipRequestSerializer(membership_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MembershipRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for MembershipRequest model.
    Only admins of a group can approve or reject requests for that group.
    Regular users can list or retrieve only their own requests,
    or requests in their admin groups.
    """

    serializer_class = MembershipRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        The user sees:
        - requests in groups where they are admin,
        - their own membership requests.
        """
        user = self.request.user
        admin_groups = GroupMembership.objects.filter(
            user=user, role=GroupMembership.Role.ADMIN
        ).values_list("group_id", flat=True)

        return MembershipRequest.objects.filter(
            Q(group_id__in=admin_groups) | Q(user=user)
        ).distinct()

    @action(detail=True, methods=["post"], permission_classes=[IsGroupAdmin])
    def approve(self, request, pk=None):
        """
        Approve the membership request.
        Only the group admin is allowed to do this.
        """
        membership_request = self.get_object()
        membership_request.approve()
        return Response({"detail": "Request approved"})

    @action(detail=True, methods=["post"], permission_classes=[IsGroupAdmin])
    def reject(self, request, pk=None):
        """
        Reject the membership request.
        Only the group admin is allowed to do this.
        """
        membership_request = self.get_object()
        membership_request.reject()
        return Response({"detail": "Request rejected"})
