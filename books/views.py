from django.shortcuts import render
from .serializers import *
from .models import *

from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status


# 책 제목 검색
@api_view(['GET'])
def book_title_search(request, book_name):
    if request.method == 'GET':
        try:
            # 대소문자 구분 없이 책 제목 검색
            books = Book.objects.filter(title__icontains=book_name)
            
            # 여러 개의 책을 직렬화합니다.
            serializer = BookSerializer(books, many=True)
            
            return Response({
                "code": status.HTTP_200_OK,
                "msg": "success",
                "data": serializer.data  # 직렬화된 데이터 반환
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "code": status.HTTP_404_NOT_FOUND,
                "msg": str(e)  # 예외 메시지 반환
            }, status=status.HTTP_404_NOT_FOUND)
        

# 책 id값으로 검색
@api_view(['GET'])
def book_id_search(request, book_id):
    if request.method == 'GET':
        try:
            # 주어진 ID로 책 검색
            book = Book.objects.get(id=book_id)
            
            # 책 정보를 직렬화합니다.
            serializer = BookSerializer(book)
            
            return Response({
                "code": status.HTTP_200_OK,
                "msg": "success",
                "data": serializer.data  # 직렬화된 데이터 반환
            }, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({
                "code": status.HTTP_404_NOT_FOUND,
                "msg": "Book not found"  # 책이 존재하지 않을 경우 메시지 반환
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "msg": str(e)  # 예외 메시지 반환
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)