from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
# Create your models here.

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICE = sorted([(item[1][0],item[0]) for item in LEXERS])
STYLE_CHOICE = sorted((item,item)for item in get_all_styles())


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100,blank=True,default='')
    code = models.TextField()
    lineos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICE,default='python',max_length=100)
    style = models.CharField(choices=STYLE_CHOICE,default='friendly',max_length=100)

    class Meta:
        ordering = ('created',)


class UserInfo(models.Model):
    USER_TYPE = (
        (1,'普通用户'),
        (2,'VIP'),
        (3,'SVIP')
    )
    user_type = models.IntegerField(choices=USER_TYPE)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)



class UserToken(models.Model):
    user = models.OneToOneField(UserInfo,on_delete=models.CASCADE)
    token = models.CharField(max_length=64)