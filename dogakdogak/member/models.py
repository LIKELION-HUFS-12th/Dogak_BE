from django.db import models

# Create your models here.



class CustomUser(models.Model):
    REQUIRED_FIELDS=[]
    user_id=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    name=models.CharField(max_length=20)
    gender=models.CharField(max_legnth=10)
    age=models.IntegerField()
    region=models.CharField(max_length=20)
    email=models.CharField(max_length=30)

