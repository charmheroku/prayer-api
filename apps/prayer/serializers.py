from rest_framework import serializers
from .models import Prayer, PrayerCategory, Group, GroupMembership


class PrayerCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrayerCategory
        fields = ["id", "name", "description", "created_at"]
        read_only_fields = ["created_at"]


class PrayerSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Prayer
        fields = [
            "id",
            "title",
            "content",
            "author",
            "author_name",
            "category",
            "category_name",
            "status",
            "privacy_level",
            "group",
            "prayer_count",
            "is_anonymous",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "author",
            "prayer_count",
            "created_at",
            "updated_at",
        ]

    def get_author_name(self, obj):
        if obj.is_anonymous:
            return "Anonymous"
        return obj.author.get_full_name() or obj.author.email

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None


class GroupSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = [
            "id",
            "name",
            "description",
            "is_private",
            "created_by",
            "member_count",
            "created_at",
        ]
        read_only_fields = ["created_by", "created_at"]

    def get_member_count(self, obj):
        return obj.members.count()


class GroupMembershipSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = GroupMembership
        fields = [
            "id",
            "user",
            "user_email",
            "user_name",
            "group",
            "role",
            "joined_at",
        ]
        read_only_fields = ["joined_at"]

    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.email
