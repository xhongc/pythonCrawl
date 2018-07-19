from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from api.tools import get_cookies, get_order, get_dayorder, get_monthorder, PeaceBank
from rest_framework import mixins
import json, time
from qmf_api.serializers import QmforderSerializer, GCodeSerializer, UpOrderSerializer, AddOrderSerializer
from rest_framework.response import Response
from api.serializers import UserSerializer, UserUpdateSerializer, AdminUserSerializer, LoginSerializer
from api.models import UserAdmin
from qmf_api.tools import get_data, applyCode, for_api, get_all_data
from qmf_api.models import Wxsession, OrderList
from datetime import datetime, date
from django.core import serializers
from rest_framework import status
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict, namedtuple
from django.db.models import Sum


class GoodsPagination(PageNumberPagination):
    '''
    商品列表自定义分页
    '''
    # 默认每页显示的个数
    page_size = 10
    # 可以动态改变每页显示的个数
    page_size_query_param = 'page_size'
    # 页码参数
    page_query_param = 'page'
    # 最多能显示多少页
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('total_page', int(self.page.paginator.count // 10) + 1),
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class QmfOrderViewsets(viewsets.GenericViewSet):
    serializer_class = QmforderSerializer

    def create(self, request):
        username = request.data.get('username', None)
        page = request.data.get('page', '1')
        trade_type = request.data.get('trade_type', None)
        switch = request.data.get('switch', '1')

        billDate = request.data.get('billDate', '1')
        if billDate == '1':
            default_billDate = datetime.now().strftime('%Y-%m-%d')
        else:
            default_billDate = billDate
        start_date = request.data.get('start_date', None)
        if start_date:
            start_date = int(start_date) / 1000
            start_date = time.localtime(start_date)
            start_date = time.strftime("%Y-%m-%d", start_date)

        end_date = request.data.get('end_date', None)
        if end_date:
            end_date = int(end_date) / 1000
            end_date = time.localtime(end_date)
            end_date = time.strftime("%Y-%m-%d", end_date)

        serach_type = request.data.get('serach_type', 'now')
        page_size = request.data.get('page_size', '15')
        # 实时查询
        if switch == 'fail':
            data = {'code': '12136', 'data': []}
            return JsonResponse(data)
        # 分成实时查询 与历史查询，避免频繁爬
        if serach_type == 'now':

            # user = UserAdmin.objects.filter(username=username).first()
            # reqmid = user.reqmid
            # print(reqmid)

            wx = UserAdmin.objects.filter(username=username).first()
            # 没有username 情况 返回全部
            if wx:
                wx_session = wx.url
                # print(wx_session)
                # data = get_data(wx_session=wx_session, reqmid=reqmid, page=page, trade_type=trade_type, switch=switch,
                #                 billDate=billDate)
                data = get_all_data(wx_session, page)
                # print('data:', data)
                data_list = data['data']
                # 保存数据库
                for each in data_list:
                    each['username'] = username
                    try:
                        model = OrderList.objects.create(**each)
                        model.save()
                    except BaseException as e:
                        continue
            else:
                pass

            try:
                # 没有username调全部数据
                if username:

                    if trade_type:
                        model = OrderList.objects.filter(username=username, c_time__startswith=default_billDate,
                                                         trade_type=trade_type).order_by('-id')
                    else:
                        model = OrderList.objects.filter(username=username,
                                                         c_time__startswith=default_billDate).order_by(
                            '-id')
                else:
                    if trade_type:
                        model = OrderList.objects.filter(c_time__startswith=default_billDate,
                                                         trade_type=trade_type).order_by('-id')
                    else:
                        model = OrderList.objects.filter(c_time__startswith=default_billDate).order_by(
                            '-id')
                # data = serializers.serialize('json', model)
                # data = json.loads(data, encoding='utf-8')
                # print(list(data))
                # 列表化 queryset[]
                items = model.values()
                res = list(items)
                # print(res)
                # 分页功能 object_list 返回列表数据
                p = Paginator(res, page_size)
                result = p.page(page)
                # print(result.object_list)
                res = result.object_list
                # 总页数
                total_page = p.num_pages
                count = p.count
                # res = json.dumps(res, ensure_ascii=False)
                # 聚合函数aggregate 统计
                total_money = model.aggregate(total_money=Sum('pay_money'))
                data = {}
                data['code'] = '000000'
                data['data'] = res
                data['total_page'] = total_page
                data['count'] = count
                data['total_money'] = total_money['total_money']
                # return JsonResponse(data, safe=False)
                return JsonResponse(data)

            except BaseException as e:
                data = {'code': 112, 'msg': '错了'}
                print(e)
                return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

        else:
            try:
                if billDate:
                    start_date = start_date + ' 00:00:00'
                    end_date = end_date + ' 23:59:59'
                    if username:
                        if trade_type:
                            model = OrderList.objects.filter(username=username, c_time__range=(start_date, end_date),
                                                             trade_type=trade_type).order_by('-id')
                        else:
                            # start_date = datetime(2018, 7, 16, 00, 00, 00)
                            # end_date = datetime(2018, 7, 17, 23, 59, 59)

                            model = OrderList.objects.filter(username=username,
                                                             c_time__range=(start_date, end_date)).order_by('-id')
                    else:
                        if trade_type:
                            model = OrderList.objects.filter(c_time__range=(start_date, end_date),
                                                             trade_type=trade_type).order_by('-id')
                        else:
                            # start_date = datetime(2018, 7, 16, 00, 00, 00)
                            # end_date = datetime(2018, 7, 17, 23, 59, 59)

                            model = OrderList.objects.filter(
                                c_time__range=(start_date, end_date)).order_by('-id')
                    # data = serializers.serialize('json', model)
                    # data = json.loads(data, encoding='utf-8')
                    # print(list(data))
                    items = model.values()
                    res = list(items)
                    # print(res)
                    p = Paginator(res, page_size)
                    result = p.page(page)
                    # print(result.object_list)
                    res = result.object_list

                    total_page = p.num_pages
                    count = p.count
                    # res = json.dumps(res, ensure_ascii=False)
                    total_money = model.aggregate(total_money=Sum('pay_money'))

                    data = {}
                    data['code'] = '000000'
                    data['data'] = res
                    data['total_page'] = total_page
                    data['count'] = count
                    data['total_money'] = total_money['total_money']
                    # return JsonResponse(data, safe=False)
                    return JsonResponse(data)
                data = {'code': 11, 'msg': '时间'}
                return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
            except BaseException as e:
                data = {'code': 112, 'msg': '错愕了'}
                print(e)
                return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)


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


class AddOrderViewsets(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = AddOrderSerializer
    queryset = OrderList.objects.all().order_by('id')
    pagination_class = GoodsPagination
