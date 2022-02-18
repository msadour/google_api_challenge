"""Urls file."""

from .views import MailViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"mail", MailViewSet, basename="mail")

urlpatterns = router.urls
