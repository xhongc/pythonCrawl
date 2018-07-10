from django.db import models


# Create your models here.
class Wxsession(models.Model):
    wx_session = models.CharField('wx_session', max_length=65, blank=True, null=True)

    class Meta:
        verbose_name = "微信授权"
        verbose_name_plural = verbose_name
