from django.db import models  # noqa: F401
from django.utils.translation import gettext_lazy as _
from apps.users.models import User


class PrayerCategory(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    description = models.TextField(_("Description"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_categories",
    )

    class Meta:
        verbose_name = _("Prayer Category")
        verbose_name_plural = _("Prayer Categories")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Prayer(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", _("Active")
        ANSWERED = "answered", _("Answered")
        ARCHIVED = "archived", _("Archived")

    class PrivacyLevel(models.TextChoices):
        PUBLIC = "public", _("Public")
        PRIVATE = "private", _("Private")
        GROUP = "group", _("Group Only")

    title = models.CharField(_("Title"), max_length=200)
    content = models.TextField(_("Content"))
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="prayers"
    )
    category = models.ForeignKey(
        PrayerCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="prayers",
    )
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.ACTIVE
    )
    privacy_level = models.CharField(
        max_length=10,
        choices=PrivacyLevel.choices,
        default=PrivacyLevel.PUBLIC,
    )
    group = models.ForeignKey(
        "Group",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="prayers",
    )
    prayer_count = models.PositiveIntegerField(default=0)
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Prayer")
        verbose_name_plural = _("Prayers")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Group(models.Model):
    name = models.CharField(_("Name"), max_length=200)
    description = models.TextField(_("Description"), blank=True)
    is_private = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_groups"
    )
    members = models.ManyToManyField(
        User, through="GroupMembership", related_name="prayer_groups"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Prayer Group")
        verbose_name_plural = _("Prayer Groups")
        ordering = ["name"]

    def __str__(self):
        return self.name


class GroupMembership(models.Model):
    class Role(models.TextChoices):
        MEMBER = "member", _("Member")
        ADMIN = "admin", _("Admin")
        MODERATOR = "moderator", _("Moderator")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=10, choices=Role.choices, default=Role.MEMBER
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "group"]
