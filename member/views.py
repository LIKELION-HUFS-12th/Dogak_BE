from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from .models import CustomUser
from .serializers import UserSerializer
from .serializers import *

from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        



        
@api_view(['GET'])
def profileView(request, userid_pk):
    if request.method == 'GET':
        try:
            # userid_pk에 해당하는 CustomUser 객체를 필터링
            customUser = CustomUser.objects.get(id=userid_pk)  # id가 userid_pk인 사용자만 가져옴
            serializer = ProfileSerializer(customUser)  # 단일 객체이므로 many=False
            return Response({
                "code": status.HTTP_200_OK,
                "msg": "Success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({
                "code": status.HTTP_404_NOT_FOUND,
                "msg": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:  # 다른 예외 처리
            return Response({
                "code": status.HTTP_400_BAD_REQUEST,
                "msg": "error"
            }, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
def how_many_books(request, userid_pk):
    try:
        # userid_pk로 사용자 가져오기
        user = CustomUser.objects.get(pk=userid_pk)
    except CustomUser.DoesNotExist:
        return Response({
            "code": status.HTTP_404_NOT_FOUND,
            "msg": "User not found."
        }, status=status.HTTP_404_NOT_FOUND)

    # 사용자가 보유한 bankbooks 수 계산
    bankbook_count = Bankbook.objects.filter(user=user).count()

    return Response({
        "code": status.HTTP_200_OK,
        "msg": "Success",
        "data": {
            "user_id": userid_pk,
            "bankbook_count": bankbook_count
        }
    }, status=status.HTTP_200_OK)



from collections import Counter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def genre_ratio(request, userid_pk):
    try:
        # userid_pk로 사용자 가져오기
        user = CustomUser.objects.get(pk=userid_pk)
    except CustomUser.DoesNotExist:
        return Response({
            "code": status.HTTP_404_NOT_FOUND,
            "msg": "User not found."
        }, status=status.HTTP_404_NOT_FOUND)

    # 사용자가 보유한 bankbooks 조회
    bankbooks = Bankbook.objects.filter(user=user)

    # 각 book의 장르를 수집
    genres = [book.book.classification for book in bankbooks]

    # 장르 비율 계산
    genre_count = Counter(genres)
    total_books = len(genres)
    genre_ratio = {genre: count / total_books for genre, count in genre_count.items()} if total_books > 0 else {}

    return Response({
        "code": status.HTTP_200_OK,
        "msg": "Success",
        "data": {
            "user_id": userid_pk,
            "genre_ratio": genre_ratio
        }
    }, status=status.HTTP_200_OK)
