from django.urls import path
from .views import *

urlpatterns = [
    path('book_title/',book_click), # 책 클릭
    path('bankbook/',bankbook), # 도서 정보 확인
    path('bankbook_post',bankbook_post),


]