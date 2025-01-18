from django.urls import path
from .views import *

urlpatterns = [
    # 유저가 등록한 통장 책에 대한 데이터 전부 반환
    path('book_title/<int:userid_pk>/',book_click),

    # 유저가 등록한 독서 통장의 내용 전체 반환
    path('bankbook/<int:userid_pk>/',bankbook), # 도서 정보 확인
    path('bankbook_post/<int:userid_pk>/<int:booksid_pk>/', bankbook_post), # 독서 통장 기록하기
]