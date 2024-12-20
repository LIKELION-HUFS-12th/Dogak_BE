from django.urls import path
from .views import RegisterView, LoginView, LogoutView
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # 회원가입
    path('login/', LoginView.as_view(), name='login'),  # 로그인
    path('logout/', LogoutView.as_view(), name='logout'),  # 로그아웃

    path('profile/',profileView),
    path('howmanybooks/<int:userid_pk>/', how_many_books),
    path('genre_ratio/<int:userid_pk>/',genre_ratio),
]