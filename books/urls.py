from django.urls import path
from .views import *

urlpatterns = [
    path('book_search/<str:book_name>/',book_title_search),
    path('book_id_search/<int:book_id>/',book_id_search),
]