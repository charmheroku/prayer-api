from django.contrib import admin  # noqa: F401
from .models import (
    Prayer,
    PrayerCategory,
    Group,
    GroupMembership,
    MembershipRequest,
)


@admin.register(Prayer)
class PrayerAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "category",
        "status",
        "privacy_level",
        "created_at",
    ]
    list_filter = ["status", "privacy_level", "category", "is_anonymous"]
    search_fields = ["title", "content"]
    date_hierarchy = "created_at"


@admin.register(PrayerCategory)
class PrayerCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
    search_fields = ["name", "description"]


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ["name", "is_private", "created_by", "created_at"]
    list_filter = ["is_private"]
    search_fields = ["name", "description"]


@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ["user", "group", "role", "joined_at"]
    list_filter = ["role"]
    search_fields = ["user__email", "group__name"]


@admin.register(MembershipRequest)
class MembershipRequestAdmin(admin.ModelAdmin):
    list_display = ["user", "group", "status", "created_at", "processed_at"]
    list_filter = ["status"]
    search_fields = ["user__email", "group__name"]
