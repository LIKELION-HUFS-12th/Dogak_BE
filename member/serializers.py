from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from bankbook.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'name', 'gender', 'age', 'region', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'gender', 'age']


class CustomUserSerializer(serializers.ModelSerializer):
    read_books_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'name', 'gender', 'age', 'region', 'email', 'read_books_count']

    def get_read_books_count(self, obj):
        return obj.user.count()


# 새로운 CustomTokenObtainPairSerializer 추가
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # 기본 토큰 검증
        data = super().validate(attrs)

        # 사용자 정보 추가
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'name': self.user.name,
            'email': self.user.email,
            'gender': self.user.gender,
            'age': self.user.age,
            'region': self.user.region,
        }

        return data