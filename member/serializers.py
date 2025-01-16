from rest_framework import serializers
from .models import CustomUser
from bankbook.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'userid', 'name', 'gender', 'age', 'region', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields=['username','name','gender','age']


class CustomUserSerializer(serializers.ModelSerializer):
    read_books_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'name', 'gender', 'age', 'region', 'email', 'read_books_count']

    def get_read_books_count(self, obj):
        return obj.user.count()  


    