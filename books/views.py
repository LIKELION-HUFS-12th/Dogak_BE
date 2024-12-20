from django.shortcuts import render
from .serializers import *
from .models import *

from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status


@api_view(['GET'])
def book_title_search(request, book_name):
    books = Books.objects.filter(title__icontains=book_name)  # 대소문자 구분 없이 검색
    serializer = BookSerializer(books, many=True)  # 여러 개의 책을 직렬화합니다.
    
    
    return Response(serializer.data, status=status.HTTP_200_OK)
    

