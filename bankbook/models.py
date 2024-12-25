from django.db import models
from books.models import Book
from member.models import *
# Create your models here.

class Bankbook(models.Model):
    user=models.ForeignKey(CustomUser,null=False, on_delete=models.CASCADE,related_name='user')
    book = models.ForeignKey(Book, null=False, on_delete=models.CASCADE,related_name='books')
    sentence = models.CharField(max_length=100)
    body = models.CharField(max_length=1000)
    start_date=models.DateTimeField()

    start_page=models.IntegerField()
    end_page=models.IntegerField()
    last_page=models.IntegerField()

    def save(self, *args, **kwargs):
        # end_page가 설정될 때 last_page를 갱신
        if self.end_page is not None:
            self.last_page = self.end_page
        super().save(*args, **kwargs)
