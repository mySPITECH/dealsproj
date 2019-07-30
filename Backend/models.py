from django.db import models

# Create your models here.
class EmailToken(models.Model):
    token= models.CharField(max_length=50)
    uid = models.BigIntegerField()