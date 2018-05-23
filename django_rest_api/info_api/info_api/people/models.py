from django.db import models


# Create your models here.
class People(models.Model):
    username = models.CharField('姓名', max_length=30, null=True, blank=True)
    money = models.CharField('金额', max_length=30, null=True, blank=True)
