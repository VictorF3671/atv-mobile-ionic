# presenca/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, PresencaViewSet, LoginView

router = DefaultRouter()
router.register("usuarios", UserViewSet, basename="usuarios")
router.register("presencas", PresencaViewSet, basename="presencas")

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("", include(router.urls)),
]
