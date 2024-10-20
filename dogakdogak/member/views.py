from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .serializers import SignupSerializer, UserSerializer
from .models import CustomUser
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.exceptions import TokenError
from datetime import datetime

class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # perform_create 메서드를 호출하여 사용자 데이터를 생성
        user_data = serializer.save()  # request 인수를 전달하지 않고 호출

        # Prepare the response data
        return Response(user_data, status=status.HTTP_201_CREATED)

    
    
class LoginView(TokenObtainPairView):  # Use Custom serializer
    permission_classes = [permissions.AllowAny]

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return Response({"detail": "Authorization header is required."}, status=status.HTTP_400_BAD_REQUEST)

            access_token = auth_header.split(' ')[1]
            token = AccessToken(access_token)

            # OutstandingToken 인스턴스 생성 또는 검색
            outstanding_token, created = OutstandingToken.objects.get_or_create(
                token=str(token),
                defaults={
                    'expires_at': datetime.fromtimestamp(token['exp']),
                    'jti': token['jti'],
                    'user': request.user,
                }
            )

            # BlacklistedToken 인스턴스 생성
            BlacklistedToken.objects.get_or_create(
                token=outstanding_token
            )

            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer