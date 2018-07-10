from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from api.tools import get_cookies, get_order, get_dayorder, get_monthorder, PeaceBank
from rest_framework import mixins
import json
from qmf_api.serializers import QmforderSerializer
from rest_framework.response import Response
from api.serializers import UserSerializer, UserUpdateSerializer, AdminUserSerializer, LoginSerializer
from api.models import UserAdmin

from qmf_api.tools import get_data
from qmf_api.models import Wxsession


class QmfOrderViewsets(viewsets.GenericViewSet):
    serializer_class = QmforderSerializer

    def list(self, request):
        username = request.session.get('username')
        print('I am :  ', username)
        if username:
            user = UserAdmin.objects.filter(username=username).first()
            reqmid = user.reqmid
            print(reqmid)
            wx = Wxsession.objects.order_by('-id').first()
            wx_session = wx.wx_session
            print(wx_session)
            data = get_data(wx_session=wx_session, reqmid=reqmid)
        else:
            data = {'code': 11, 'msg': '账号未登录'}
        return JsonResponse(data)

    def create(self, request):
        username = request.session.get('username')
        page = request.data.get('page', '1')
        trade_type = request.data.get('trade_type', '')
        switch = request.data.get('switch', '1')
        print(trade_type)
        # print('I am :  ', username)
        if username:
            user = UserAdmin.objects.filter(username=username).first()
            reqmid = user.reqmid
            # print(reqmid)
            wx = Wxsession.objects.order_by('-id').first()
            wx_session = wx.wx_session
            # print(wx_session)
            data = get_data(wx_session=wx_session, reqmid=reqmid, page=page, trade_type=trade_type, switch=switch)
        else:
            data = {'code': 11, 'msg': '账号未登录'}
        return JsonResponse(data)
