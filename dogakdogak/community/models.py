from django.db import models
from member.models import CustomUser
# Create your models here.



class Community_by_book(models.Model):
    title=models.CharField(max_length=30)
    body=models.CharField(max_length=200)
    period=models.CharField(max_length=30)
    status=models.CharField(max_length=10)

    participant=models.ManyToManyField(CustomUser,on_delete=models.CASCADE)
    leader=models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    book_title=models.CharField(max_length=20,null=True)
    book_author=models.CharField(max_length=20,null=True)
    book_cheonggu=models.CharField(max_length=20,null=True)
    book_publisher=models.CharField(max_length=20,null=True)


class Community_by_period(models.Model):
    pass


class User_page(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    community=models.ForeignKey(Community_by_book,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    page=models.IntegerField()
    
    
    
    
    