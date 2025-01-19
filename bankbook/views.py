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




@api_view(['POST'])
def bankbook_post(request, userid_pk, booksid_pk):  # userid_pk와 books_pk를 인자로 추가
    try:
        # 사용자와 책을 가져오기
        user = CustomUser.objects.get(pk=userid_pk)  # userid_pk로 사용자 가져오기
        book = Book.objects.get(pk=booksid_pk)  # books_pk로 책 가져오기
    except (CustomUser.DoesNotExist, Book.DoesNotExist) as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # serializer에 user와 book을 포함하여 저장
    serializer = BankbookPostSerializer(data=request.data)
    if serializer.is_valid():
        # user와 book을 serializer에 설정
        instance = serializer.save(user=user, book=book)  # user와 book을 설정하여 인스턴스 저장
        return Response({
            "code": status.HTTP_201_CREATED,
            "msg": "Created",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Bankbook  # Bankbook 모델을 가져옵니다.
from .serializers import MonthlyReadingCountSerializer, WeeklyReadingCountSerializer, YearlyReadingCountSerializer
from django.db.models import Count
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Bankbook  # Bankbook 모델을 가져옵니다.
from .serializers import MonthlyReadingCountSerializer, WeeklyReadingCountSerializer, YearlyReadingCountSerializer
from django.db.models import Count
from django.db.models.functions import ExtractMonth, ExtractWeek, ExtractYear  # 필요한 함수 임포트
from django.utils import timezone

class MonthlyReadingCountView(APIView):
    def get(self, request, userid_pk):
        current_year = timezone.now().year
        monthly_counts = (
            Bankbook.objects.filter(user_id=userid_pk)
            .annotate(month=ExtractMonth('start_date'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )
        serializer = MonthlyReadingCountSerializer(monthly_counts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class WeeklyReadingCountView(APIView):
    def get(self, request, userid_pk):
        current_year = timezone.now().year
        weekly_counts = (
            Bankbook.objects.filter(user_id=userid_pk)
            .annotate(week=ExtractWeek('start_date'))
            .values('week')
            .annotate(count=Count('id'))
            .order_by('week')
        )
        serializer = WeeklyReadingCountSerializer(weekly_counts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class YearlyReadingCountView(APIView):
    def get(self, request, userid_pk):
        yearly_counts = (
            Bankbook.objects.filter(user_id=userid_pk)
            .annotate(year=ExtractYear('start_date'))
            .values('year')
            .annotate(count=Count('id'))
            .order_by('year')
        )
        serializer = YearlyReadingCountSerializer(yearly_counts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
