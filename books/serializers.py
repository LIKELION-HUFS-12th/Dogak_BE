from rest_framework import serializers
from .models import *


class BookSerializer(serialziers.ModelSerializer):
    class Meta:
        model=Books
        fields=['title','author','publisher','publish_year','isbn','classification_number','classification']


