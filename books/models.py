from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)  # 도서명
    author = models.CharField(max_length=255)  # 저자
    publisher = models.CharField(max_length=255)  # 출판사
    publish_year = models.IntegerField()  # 발행년도
    isbn = models.CharField(max_length=13, unique=True)  # ISBN
    classification_number = models.FloatField()  # 주제분류번호
    classification = models.CharField(max_length=50)  # 주제분류

    def __str__(self):
        return self.title