from django.urls import path
from .views import *

urlpatterns = [
    path('book_title/<int:userid_pk>/',book_click), # 책 클릭
    path('bankbook/<str:userid_pk>/',bankbook), # 도서 정보 확인
    path('bankbook_post/<int:userid_pk>/<int:booksid_pk>/', bankbook_post), # 독서 통장 기록하기


]