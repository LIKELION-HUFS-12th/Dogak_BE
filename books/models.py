from django.db import models

# Create your models here.

class Books(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    publish_year = models.IntegerField()
    isbn = models.IntegerField()
    classification_number = models.FloatField()
    classification = models.CharField(max_length=10)
