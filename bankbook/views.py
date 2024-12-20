from django.shortcuts import render
from .serializers import *
from .models import *

from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status


@api_view(['GET'])
def book_click(request,userid_pk):
    if request.method=='GET':
        try:
            bankbooks = Bankbook.objects.filter(user_id=userid_pk)

            serializer = BooktitleSerializer(bankbooks, many=True)  
            return Response({
                "code": status.HTTP_200_OK,
                "msg": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "code": status.HTTP_404_NOT_FOUND,
                "msg": str(e)  # 예외 메시지 반환
            }, status=status.HTTP_404_NOT_FOUND)


# @api_view(['GET'])
# def bankbook(request):
#     if request.method=='GET':
#         try:
#             bankbook=Bankbook.objects.all()
#             serializer=BankbookSerializer(bankbook,many=True)
#             return Response({
#                 "code": status.HTTP_200_OK,
#                 "msg": "Success",
#                 "data": serializer.data
#             }, status=status.HTTP_200_OK)
#         except:
#             return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def bankbook(request, userid_pk):  # userid_pk를 인자로 추가
    if request.method == 'GET':
        try:
            # userid_pk에 해당하는 Bankbook 객체를 필터링
            bankbook = Bankbook.objects.filter(user_id=userid_pk)  # user_id가 userid_pk인 Bankbook만 가져옴
            serializer = BankbookSerializer(bankbook, many=True)
            return Response({
                "code": status.HTTP_200_OK,
                "msg": "Success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:  # 예외 발생 시 에러 메시지를 포함
            return Response({
                "code": status.HTTP_400_BAD_REQUEST,
                "msg": "error"  # 에러 메시지를 반환
            }, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def bankbook_post(request):
#     serializer = BankbookPostSerializer(data=request.data)
#     if serializer.is_valid():
#         instance = serializer.save()
#         return Response({
#             "code": status.HTTP_201_CREATED,
#             "msg": "Created",
#             "data": {
#                 "id": instance.id,  # 생성된 인스턴스의 ID
#                 "nickname": request.data.get("nickname", ""),  # 요청 데이터에서 nickname 가져오기
#                 "email": request.data.get("email", "")  # 요청 데이터에서 email 가져오기
#             }
#         }, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def bankbook_post(request, userid_pk, booksid_pk):  # userid_pk와 books_pk를 인자로 추가
    try:
        # 사용자와 책을 가져오기
        user = CustomUser.objects.get(pk=userid_pk)  # userid_pk로 사용자 가져오기
        book = Books.objects.get(pk=booksid_pk)  # books_pk로 책 가져오기
    except (CustomUser.DoesNotExist, Books.DoesNotExist) as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # serializer에 user와 book을 포함하여 저장
    serializer = BankbookPostSerializer(data=request.data)
    if serializer.is_valid():
        # user와 book을 serializer에 설정
        instance = serializer.save(user=user, book=book)  # user와 book을 설정하여 인스턴스 저장
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




