from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from . import models
from django.views.generic.base import View
import json
from django.http import HttpResponse
from rest_framework.request import Request
from rest_framework import exceptions
from rest_framework.authentication import BasicAuthentication

# Create your views here.
ORDER_DICT = {
    1:{
        'name':'apple',
        'price':15
    },
    2:{
        'name':'dog',
        'price':100
    }
}

def md5(user):
    import hashlib
    import time
    ctime = str(time.time())
    m = hashlib.md5(bytes(user,encoding='utf-8'))
    m.update(bytes(ctime,encoding='utf-8'))

    return m.hexdigest()



class AuthView(View):
    def get(self,request):
        ret = {'code': 1000, 'msg': None}
        return JsonResponse(ret)
    def post(self,request,*args,**kwargs):
        ret = {'code':1000,'msg':None}
        try:
            user = request.POST.get('username')
            pwd = request.POST.get('password')
            obj = models.UserInfo.objects.filter(username=user,password=pwd).first()
            if not obj:
                ret['code'] = 1001
                ret['msg'] = u'用户名或密码错误'
            token = md5(user)
            models.UserToken.objects.update_or_create(user=obj,defaults={'token':token})
            ret['token'] = token
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = u'请求异常'
            print(e)
        return HttpResponse(json.dumps(ret,ensure_ascii=False), content_type="application/json")

class Authentication(APIView):
    '''认证'''
    def authenticate(self,request):
        token = request._request.GET.get('token')
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败')
        #在rest framework内部会将这两个字段赋值给request，以供后续操作使用
        return (token_obj.user,token_obj)

    def authenticate_header(self, request):
        pass


class OrderView(APIView):
    authentication_classes = [Authentication,]
    def get(self,request,*args,**kwargs):
        ret = {'code':1000,'msg':None,'data':None}
        try:
            ret['data'] = ORDER_DICT
        except Exception as e:
            pass
        return JsonResponse(ret)