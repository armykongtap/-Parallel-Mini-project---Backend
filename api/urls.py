from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import LoginViewSet, GroupViewSet, JoinViewSet

router = DefaultRouter()
router.register(r'login', LoginViewSet, basename='login')
router.register(r'group', GroupViewSet, basename='group')
router.register(r'join', JoinViewSet, basename='join_group')

urlpatterns = router.urls