from rest_framework import serializers
from .models import *


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=['title','author','publisher','publish_year','isbn','classification_number','classification']