#为应用程序users定义URL模式
from django.conf.urls import url
from django.contrib.auth.views import login

from . import  views

urlpatterns= [
    url(r'^login/$',login,{'template_name':'users/login.html'},
        name = 'login'),
    #注销
    url(r'^logout/$',views.logout_view,name = 'logout'),
    #注册页面
    url(r'^register/$',views.register,name='register'),
]