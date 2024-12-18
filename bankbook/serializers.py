from rest_framework import serializers
from .models import *

class BooktitleSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    class Meta:
        model = Bankbook
        fields = ['book.title']


class BankbookSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    
    class Meta:
        model=Bankbook
        fields=['page','book_title','sentence','body']


class BankbookPostSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = Bankbook
        fields = ['page','book_title', 'sentence', 'body', 'start_date'] 


class DateInputSerializer(serializers.Serializer):
    date = serializers.DateField()

