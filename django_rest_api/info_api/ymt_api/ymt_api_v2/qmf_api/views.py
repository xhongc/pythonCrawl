from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from api.tools import get_cookies, get_order, get_dayorder, get_monthorder, PeaceBank
from rest_framework import mixins
import json
from qmf_api.serializers import QmforderSerializer, GCodeSerializer, UpOrderSerializer
from rest_framework.response import Response
from api.serializers import UserSerializer, UserUpdateSerializer, AdminUserSerializer, LoginSerializer
from api.models import UserAdmin
from qmf_api.tools import get_data, applyCode, for_api
from qmf_api.models import Wxsession
from datetime import datetime


class QmfOrderViewsets(viewsets.GenericViewSet):
    serializer_class = QmforderSerializer

    def list(self, request):
        username = request.data.get('username', None)
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
        username = request.data.get('username', None)
        page = request.data.get('page', '1')
        trade_type = request.data.get('trade_type', '')
        switch = request.data.get('switch', '1')
        default_billDate = datetime.now().strftime('%Y-%m-%d')
        billDate = request.data.get('billDate', default_billDate)
        print(trade_type)
        # print('I am :  ', username)
        if username:
            user = UserAdmin.objects.filter(username=username).first()
            reqmid = user.reqmid
            # print(reqmid)
            wx = UserAdmin.objects.filter(username=username).first()
            wx_session = wx.url
            print(wx_session)
            data = get_data(wx_session=wx_session, reqmid=reqmid, page=page, trade_type=trade_type, switch=switch,
                            billDate=billDate)
        else:
            data = {'code': 11, 'msg': '账号未登录'}
        return JsonResponse(data)


class GenerateCodeViewsets(viewsets.GenericViewSet):
    serializer_class = GCodeSerializer

    def create(self, request):
        productName = request.data.get('productName', None)
        productAmout = request.data.get('productName', None)
        productId = request.data.get('productName', None)

        data = applyCode(productName, productAmout, productId)
        data = json.loads(data)
        return JsonResponse(data)


class UpOrderViewsrts(viewsets.GenericViewSet):
    serializer_class = UpOrderSerializer

    def create(self, request):
        PayNO = request.data.get('PayNO', None)
        PayJe = request.data.get('PayJe', None)
        payType = request.data.get('payType', None)
        PayMore = request.data.get('PayMore', None)

        item = {}
        item['PayNO'] = PayNO
        item['PayJe'] = PayJe
        item['payType'] = payType
        item['PayMore'] = PayMore
        data = for_api(item)

        return JsonResponse(data)
