from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, BookSearchView

router = DefaultRouter()
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('search/', BookSearchView.as_view(), name='book-search'),  # 책 검색 URL
    path('', include(router.urls)),  # 리뷰 관련 URL
]