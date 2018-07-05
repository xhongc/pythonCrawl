from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from api.tools import get_cookies, get_order, get_dayorder, get_monthorder, PeaceBank
from rest_framework import mixins
import json
from api.serializers import OrderSerializer
from rest_framework.response import Response
from api.serializers import UserSerializer, UserUpdateSerializer, AdminUserSerializer, LoginSerializer
from api.models import UserAdmin
from django.contrib.auth import login, authenticate
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from django.contrib.auth import get_user_model
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict, namedtuple
import random
from qmf_api.tools import get_data


class QmfOrderViewsets(viewsets.GenericViewSet):
    def list(self, request):
        username = request.session.get('username')
        if username:
            user = UserAdmin.objects.filter(username=username).first()
            # 还没创建
            reqmid = user.reqmid
            # 新建个表 wxsession
            wx = Wxsession.objects.order_by(-id).first()
            wx_session = wx.wxssion
            data = get_data(wx_session=wx_session, reqmid=reqmid)

            return JsonResponse(data)
        else:
            data = {'code': 11, 'msg': '账号未登录'}
