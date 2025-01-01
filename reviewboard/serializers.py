from rest_framework import serializers
from .models import Review
from books.models import Book

class ReviewSerializer(serializers.ModelSerializer):
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        source='book',
        write_only=True,
        required=False
    )
    book = serializers.StringRelatedField(read_only=True)
    custom_book_title = serializers.CharField(max_length=255, required=False)
    custom_book_author = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = Review
        fields = [
            'id', 'user', 'book_id', 'book', 'custom_book_title', 'custom_book_author',
            'review_title', 'review_content', 'rating', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate(self, data):
        # 책 선택 여부 확인
        if not data.get('book') and not data.get('custom_book_title'):
            raise serializers.ValidationError("책을 선택하거나 직접 입력해야 합니다.")
        if not data.get('book') and not data.get('custom_book_author'):
            raise serializers.ValidationError("저자를 입력해야 합니다.")
        return data