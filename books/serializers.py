from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    # SerializerMethodField를 사용해 image_url 필드를 추가
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'  # 모든 필드 포함

    def get_image_url(self, obj):
        """
        ISBN을 기반으로 이미지 URL 생성
        """
        return f'https://contents.kyobobook.co.kr/sih/fit-in/458x0/pdt/{obj.isbn}.jpg'