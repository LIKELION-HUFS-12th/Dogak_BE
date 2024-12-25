from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GroupBoardViewSet

router = DefaultRouter()
router.register(r'', GroupBoardViewSet, basename='groupboard')

urlpatterns = [
    path('', include(router.urls)),
    path('join/<int:group_id>/', GroupBoardViewSet.as_view({'post': 'add_participant'}), name='join-groupboard'),
]