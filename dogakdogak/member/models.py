from django.db import models

# Create your models here.



class CustomUser(models.Model):
    REQUIRED_FIELDS=[]
    user_id=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    name=models.CharField(max_length=20)
    gender=models.CharField(max_length=10)
    age=models.IntegerField()
    region=models.CharField(max_length=20)
    email=models.CharField(max_length=30)

class UserBooklist(models.Model):
    user=models.ForeignKey(CustomUser,related_name="booklist",on_delete=models.CASCADE)

    title=models.CharField(max_length=20)
    body=models.CharField(max_length=1000)
    star=models.IntegerField()

    # BookList 테이블을 안 만드는 상황이라서 일단 CharField로 만들었습니다.
    book_title=models.CharField(max_length=20)
    book_author=models.CharField(max_length=20)
    book_cheonggu=models.CharField(max_length=20)
    book_publisher=models.CharField(max_length=20)