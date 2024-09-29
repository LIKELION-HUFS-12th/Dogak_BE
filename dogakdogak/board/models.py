from django.db import models
from member.models import CustomUser
# Create your models here.


class Board(models.Model):
    title=models.CharField(max_length=30)
    body=models.CharField(max_length=1000)
    date=models.DateTimeField(auto_now_add=True)
    writer=models.ForeignKey(CustomUser,on_delete=models.CASCADE)


class Comment(models.Model):
    body=models.CharField(max_length=1000)
    date=models.DateTimeField(auto_now_add=True)
    board=models.ForeignKey(Board,on_delete=models.CASCADE)
    writer=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    


