from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import hello, LoginViewSet

router = DefaultRouter()
router.register(r'login', LoginViewSet, basename='login')

urlpatterns = router.urls