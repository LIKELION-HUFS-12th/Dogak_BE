from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from .models import CustomUser
from .serializers import UserSerializer, CustomTokenObtainPairSerializer, ProfileSerializer
from rest_framework.decorators import api_view
from bankbook.models import Bankbook
from collections import Counter


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        # 사용자 생성
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # 사용자 저장
        
        # 토큰 생성
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # 응답 데이터 구성
        response_data = {
            "code": status.HTTP_201_CREATED,
            "msg": "User registered successfully.",
            "data": serializer.data,
            "tokens": {
                "access": access_token,
                "refresh": refresh_token
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
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
    try:
        # 사용자 정보 조회
        customUser = CustomUser.objects.get(id=userid_pk)
        serializer = ProfileSerializer(customUser)
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
    except Exception:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "msg": "error"
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def how_many_books(request, userid_pk):
    try:
        user = CustomUser.objects.get(pk=userid_pk)
    except CustomUser.DoesNotExist:
        return Response({
            "code": status.HTTP_404_NOT_FOUND,
            "msg": "User not found."
        }, status=status.HTTP_404_NOT_FOUND)

    bankbook_count = Bankbook.objects.filter(user=user).count()

    return Response({
        "code": status.HTTP_200_OK,
        "msg": "Success",
        "data": {
            "user_id": userid_pk,
            "bankbook_count": bankbook_count
        }
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def genre_ratio(request, userid_pk):
    try:
        user = CustomUser.objects.get(pk=userid_pk)
    except CustomUser.DoesNotExist:
        return Response({
            "code": status.HTTP_404_NOT_FOUND,
            "msg": "User not found."
        }, status=status.HTTP_404_NOT_FOUND)

    bankbooks = Bankbook.objects.filter(user=user)
    genres = [book.book.classification for book in bankbooks]
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