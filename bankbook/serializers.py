from rest_framework import serializers
from .models import *


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=['title','author','publisher','publish_year','isbn','classification_number','classification']


class BooktitleSerializer(serializers.ModelSerializer):
    book_details=BookSerializer(source='book',read_only=True)
    class Meta:
        model = Bankbook
        fields = ['book_details']


class BankbookSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    
    class Meta:
        model=Bankbook
        fields=['book_title','sentence','body','start_page','end_page']


class BankbookPostSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    last_page = serializers.IntegerField(required=False)
    class Meta:
        model = Bankbook
        fields = ['book_title', 'sentence', 'body', 'start_date','start_page','end_page','last_page'] 

    def create(self, validated_data):
        # end_page가 제공되었는지 확인하고 last_page 설정
        end_page = validated_data.get('end_page')
        if end_page is not None:
            validated_data['last_page'] = end_page
        else:
            validated_data['last_page'] = 0  # 기본값 설정 (필요에 따라 조정 가능)

        return super().create(validated_data)

class DateInputSerializer(serializers.Serializer):
    date = serializers.DateField()

