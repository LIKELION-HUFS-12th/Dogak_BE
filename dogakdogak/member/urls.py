from django.urls import path
from .views import SignupView, LogoutView, UserInfoView, UserPostsView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'member'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]