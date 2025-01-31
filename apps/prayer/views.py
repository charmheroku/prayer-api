from django.shortcuts import render  # noqa: F401
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Prayer, PrayerCategory, Group, GroupMembership
from apps.prayer.serializers import (
    PrayerSerializer,
    PrayerCategorySerializer,
    GroupSerializer,
    GroupMembershipSerializer,
)
from apps.prayer.permissions import IsGroupMember, IsGroupAdmin


class PrayerViewSet(viewsets.ModelViewSet):
    serializer_class = PrayerSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Prayer.objects.filter(
            Q(privacy_level=Prayer.PrivacyLevel.PUBLIC)
            | Q(author=user)
            | Q(group__members=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"])
    def pray(self, request, pk=None):
        prayer = self.get_object()
        prayer.prayer_count += 1
        prayer.save()
        return Response({"status": "prayer counted"})


class PrayerCategoryViewSet(viewsets.ModelViewSet):
    queryset = PrayerCategory.objects.all()
    serializer_class = PrayerCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Group.objects.filter(
            Q(is_private=False) | Q(members=user)
        ).distinct()

    def perform_create(self, serializer):
        group = serializer.save(created_by=self.request.user)
        GroupMembership.objects.create(
            user=self.request.user,
            group=group,
            role=GroupMembership.Role.ADMIN,
        )

    @action(detail=True, methods=["post"])
    def join(self, request, pk=None):
        group = self.get_object()
        if group.is_private:
            return Response(
                {"error": "This group is private"},
                status=status.HTTP_403_FORBIDDEN,
            )
        GroupMembership.objects.get_or_create(
            user=request.user,
            group=group,
            defaults={"role": GroupMembership.Role.MEMBER},
        )
        return Response({"status": "joined group"})
