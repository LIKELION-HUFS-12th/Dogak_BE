from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    name = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    age = models.PositiveIntegerField()
    region = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username