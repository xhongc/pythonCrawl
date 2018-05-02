"""django_auth_example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
# from django.contrib import admin
from users.views import LoginView,RegisterView,ActiveUserView,ForgetPwdView,ResetView,ModifyPwdView
from organization.views import OrgView
import xadmin
from django.views.generic import TemplateView
from users import views
urlpatterns = [
    url(r'^admin/', xadmin.site.urls),
    url(r'^$',views.index,name='index'),
    url(r'^login/',LoginView.as_view(),name='login'),
    url(r'^register/',RegisterView.as_view(),name='register'),
    url(r'^captcha/',include('captcha.urls')),
    url(r'^active/(?P<active_code>.+)/',ActiveUserView.as_view(),name='user_active'),
    url(r'^forget/',ForgetPwdView.as_view(),name='forget_pwd'),
    url(r'reset/(?P<active_code>.*)/',ResetView.as_view(),name='reset_pwd'),
    url(r'^mofify_pwd/',ModifyPwdView.as_view(),name='modify_pwd'),
    url(r'^org-list/',OrgView.as_view(),name='org_list'),
]
