from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GroupBoardViewSet

router = DefaultRouter()
router.register(r'', GroupBoardViewSet, basename='groupboard')  # 기본 설정

urlpatterns = [
    path('', include(router.urls)),
]