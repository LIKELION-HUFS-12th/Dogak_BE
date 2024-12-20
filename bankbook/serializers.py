from rest_framework import serializers
from .models import *


class BookSerializer(serialziers.ModelSerializer):
    class Meta:
        model=Books
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

    class Meta:
        model = Bankbook
        fields = ['book_title', 'sentence', 'body', 'start_date','start_page','end_page','last_page'] 


class DateInputSerializer(serializers.Serializer):
    date = serializers.DateField()

