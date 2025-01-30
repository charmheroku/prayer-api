from django.shortcuts import render  # noqa: F401
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ["create", "reset_password"]:
            return [AllowAny()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        return self.serializer_class

    @action(detail=False, methods=["get"])
    def me(self, request):
        """Get current user profile."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def reset_password(self, request):
        """Initiate password reset process."""
        email = request.data.get("email")
        if email:
            try:
                user = User.objects.get(email=email)
                user.send_password_reset_email()
                return Response(
                    {"detail": "Password reset email sent"},
                    status=status.HTTP_200_OK,
                )
            except User.DoesNotExist:
                pass
        return Response(
            {"detail": "Email sent if account exists"},
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False, methods=["post"], permission_classes=[IsAuthenticated]
    )
    def change_password(self, request):
        """Change user password."""
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response(
                {"detail": "Wrong password"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()
        return Response(
            {"detail": "Password changed successfully"},
            status=status.HTTP_200_OK,
        )
