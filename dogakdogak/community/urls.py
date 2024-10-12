from django.urls import path
from .views import *
from . import views

app_name='community'


urlpatterns = [
    path('fetch_book/', fetch_book, name='fetch_book'),
]
