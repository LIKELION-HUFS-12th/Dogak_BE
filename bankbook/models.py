from django.db import models
from books.models import Books
from member.models import *
# Create your models here.

class Bankbook(models.Model):
    user=models.ForeignKey(CustomUser,null=False, on_delete=models.CASCADE,related_name='user')
    book = models.ForeignKey(Books, null=False, on_delete=models.CASCADE,related_name='books')
    page = models.IntegerField()
    sentence = models.CharField(max_length=100)
    body = models.CharField(max_length=1000)
    start_date=models.DateTimeField()
