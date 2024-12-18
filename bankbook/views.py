from django.shortcuts import render
from .serializers import *
from .models import *

from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status


@api_view(['GET'])
def book_click(request):
    if request.method=='GET':
        try:
            book_title=Bankbook.objects.all()
            serializer=BooktitleSerializer(book_title,many=True)
            return Response({
                "code": status.HTTP_200_OK,
                "msg": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def bankbook(request):
    if request.method=='GET':
        try:
            bankbook=Bankbook.objects.all()
            serializer=BankbookSerializer(bankbook,many=True)
            return Response({
                "code": status.HTTP_200_OK,
                "msg": "Success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def bankbook_post(request):
    serializer = BankbookPostSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        return Response({
            "code": status.HTTP_201_CREATED,
            "msg": "Created",
            "data": {
                "id": instance.id,  # 생성된 인스턴스의 ID
                "nickname": request.data.get("nickname", ""),  # 요청 데이터에서 nickname 가져오기
                "email": request.data.get("email", "")  # 요청 데이터에서 email 가져오기
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

