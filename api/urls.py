from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import LoginViewSet

router = DefaultRouter()
router.register(r'login', LoginViewSet, basename='login')

urlpatterns = router.urls