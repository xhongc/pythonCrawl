from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserAdmin(AbstractUser):
    url = models.CharField('url',max_length=65,blank=True, null=True)
    display_password = models.CharField('铭文密码',max_length=64,blank=True,default='0')
    ymt_name = models.CharField('用户名称', max_length=50,blank=True, null=True)
    ymt_pwd = models.CharField(max_length=64,blank=True, null=True)
    login_ip = models.CharField('IP', max_length=20, blank=True, null=True)
    last_login_time = models.CharField('登入时间', max_length=64, blank=True, null=True)

    class Meta:
        verbose_name = "用户映射"
        verbose_name_plural = verbose_name
