from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"prayers", views.PrayerViewSet, basename="prayer")
router.register(
    r"categories", views.PrayerCategoryViewSet, basename="category"
)
router.register(r"groups", views.GroupViewSet, basename="group")
router.register(
    r"membership-requests",
    views.MembershipRequestViewSet,
    basename="membership-request",
)

app_name = "prayer"

urlpatterns = [
    path("", include(router.urls)),
]
