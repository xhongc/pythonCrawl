from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from api.tools import get_cookies, get_order, get_dayorder, get_monthorder, PeaceBank
from rest_framework import mixins
import json, time
from qmf_api.serializers import QmforderSerializer, GCodeSerializer, UpOrderSerializer, AddOrderSerializer, \
    StatisticsSerializer, PaymentSerializer
from rest_framework.response import Response
from api.serializers import UserSerializer, UserUpdateSerializer, AdminUserSerializer, LoginSerializer
from api.models import UserAdmin
from qmf_api.tools import get_data, applyCode, for_api, get_all_data, get_jl_data
from qmf_api.models import Wxsession, OrderList, paymentList
from datetime import datetime, date
from django.core import serializers
from rest_framework import status
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict, namedtuple
from django.db.models import Sum
from qmf_api.gcode import LFOrder, Bill99, UlineOrder


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
        account_status = request.data.get('account_status', None)
        switch = request.data.get('switch', '1')
        billDate = request.data.get('billDate', '1')
        if billDate == '1':
            default_billDate = datetime.now().strftime('%Y-%m-%d')
        else:
            default_billDate = billDate
        start_date = request.data.get('start_date', None)
        try:
            if start_date:
                start_date = int(start_date) / 1000
                start_date = time.localtime(start_date)
                start_date = time.strftime("%Y-%m-%d %H:%M:%S", start_date)

            end_date = request.data.get('end_date', None)
            if end_date:
                end_date = int(end_date) / 1000
                end_date = time.localtime(end_date)
                end_date = time.strftime("%Y-%m-%d %H:%M:%S", end_date)
        except:
            data = {'code': '999999', 'msg': '时间错误'}
            return JsonResponse(data)

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
                channel_type = wx.channel_type
                print(channel_type)
                if channel_type == 'YL':
                    data = get_all_data(wx_session, page)
                elif channel_type == 'KU':
                    user_name = wx.ymt_name
                    user_pwd = wx.ymt_pwd
                    a = LFOrder(username=user_name, password=user_pwd)
                    data = a.get_free_data()
                    # print(data)
                elif channel_type == 'KQ':
                    a = Bill99(cookie=wx_session)
                    data = a.down_and_get_data()
                    print('daaaaaaa', data)
                elif channel_type == 'UL':
                    # user_name = wx.ymt_name
                    # user_pwd = wx.ymt_pwd
                    # a = UlineOrder(username=user_name, password=user_pwd)
                    # data = a.get_uline_data()
                    # print('111', data)
                    data = {'code': '000000', 'data': []}
                else:
                    data = {'code': '999999', 'data': []}
                # print('data:', data)
                try:
                    data_list = data['data']
                    data_code = data['code']
                    # print(data_list)
                except:
                    data_list = []
                    data_code = '998998'
                # 保存数据库
                for each in data_list:
                    each['username'] = username
                    try:
                        model = OrderList.objects.create(**each)
                        model.save()
                    except BaseException as e:
                        print('11111', e)
                        continue
            else:
                data_code = '098765'
            filter_dict = {}
            try:
                # 没有username调全部数据
                filter_dict['c_time__startswith'] = default_billDate
                if username:
                    filter_dict['username'] = username
                if trade_type:
                    filter_dict['trade_type'] = trade_type
                if account_status:
                    filter_dict['account_status'] = account_status

                model = OrderList.objects.filter(**filter_dict).order_by('-c_time')

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
                charge_total_money = model.aggregate(charge_total_money=Sum('charge'))
                total_money = total_money['total_money']
                charge_total_money = charge_total_money['charge_total_money']
                data = {}
                data['code'] = data_code
                data['data'] = res
                data['total_page'] = total_page
                data['count'] = count
                if total_money:
                    try:
                        data['total_money'] = round(float(total_money), 2)
                    except:
                        data['total_money'] = round(total_money, 2)
                else:
                    data['total_money'] = total_money
                if charge_total_money:
                    try:
                        data['charge_total_money'] = round(float(charge_total_money), 2)
                    except:
                        data['charge_total_money'] = round(charge_total_money, 2)
                else:
                    data['charge_total_money'] = charge_total_money
                return JsonResponse(data)

            except BaseException as e:
                data = {'code': 112, 'msg': '错了'}
                print('22222', e)
                return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

        else:
            filter_dict = {}

            try:
                if billDate:
                    start_date = start_date + ' 00:00:00'
                    end_date = end_date + ' 23:59:59'
                    if username:
                        filter_dict['username'] = username
                    if trade_type:
                        filter_dict['trade_type'] = trade_type
                    if account_status:
                        filter_dict['account_status'] = account_status
                    filter_dict['c_time__range'] = (start_date, end_date)
                    # print(filter_dict)
                    model = OrderList.objects.filter(**filter_dict).order_by('-id')
                    # print(model)
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
                    charge_total_money = model.aggregate(charge_total_money=Sum('charge'))
                    total_money = total_money['total_money']
                    charge_total_money = charge_total_money['charge_total_money']

                    data = {}
                    data['code'] = '000000'
                    data['data'] = res
                    data['total_page'] = total_page
                    data['count'] = count

                    if total_money:
                        try:
                            data['total_money'] = round(float(total_money), 2)
                        except:
                            data['total_money'] = round(total_money, 2)
                    else:
                        data['total_money'] = total_money

                    if charge_total_money:
                        try:
                            data['charge_total_money'] = round(float(charge_total_money), 2)
                        except:
                            data['charge_total_money'] = round(charge_total_money, 2)
                    else:
                        data['charge_total_money'] = charge_total_money

                    return JsonResponse(data)
                data = {'code': 11, 'msg': '时间'}
                return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
            except BaseException as e:
                data = {'code': 112, 'msg': 'error'}
                print(e)
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)


class GenerateCodeViewsets(viewsets.GenericViewSet):
    serializer_class = GCodeSerializer

    def create(self, request):
        login = request.data.get('login', None)
        productName = request.data.get('productName', None)
        productAmout = request.data.get('productAmout', None)
        productId = request.data.get('productId', None)
        print(productName, productAmout, productId)
        data = {}
        login_list = {
            'tingting': 'tingting123',
            'gaolei': 'gaolei123',
            'caoxinpeng': 'caoxinpeng123',
            'wangzhibin': 'wangzhibin123',
            'hushan': 'hushan123',
            'wanyijie': 'wanyijie123',
            'tingtinga': 'tingtinga123',
            'gaoleia': 'gaoleia123',
            'caoxinpenga': 'caoxinpenga123',
            'wangzhibina': 'wangzhibina123',
            'husana': 'husana123',
        }
        sid_list = {
            'tingting': '105874',
            'gaolei': '105868',
            'caoxinpeng': '105884',
            'wangzhibin': '105889',
            'hushan': '105892',
            'wanyijie': '105899',
            'tingtinga': '105905',
            'gaoleia': '105906',
            'caoxinpenga': '105908',
            'wangzhibina': '105909',
            'husana': '105910',
        }

        if login in login_list:
            username = login
            password = login_list[login]
            sid = sid_list[login]
            apikey = sid + '001'
            # data = applyCode(productName, productAmout, productId)
            a = LFOrder(username=username, password=password)
            a.gcode(beizhu=productId, money=productAmout, sid=sid, apikey=apikey)
            time.sleep(1)
            resUrl = a.get_code_url()
            # data = json.loads(data)
            data['code'] = '000000'
            data['data'] = resUrl
        else:
            data = {'code': '11', 'msg': 'bucunzai'}
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


class StatisticsViewsets(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = StatisticsSerializer

    def create(self, request, *args, **kwargs):
        trade_type = request.data.get('trade_type', None)
        channel_type = request.data.get('channel_type', None)
        start_date = request.data.get('start_date', None)
        page = request.data.get('page', '1')
        page_size = request.data.get('page_size', '15')
        filter_dict = {}
        try:
            if start_date:
                start_date = int(start_date) / 1000
                start_date = time.localtime(start_date)
                start_date = time.strftime("%Y-%m-%d 00:00:00", start_date)

            end_date = request.data.get('end_date', None)
            if end_date:
                end_date = int(end_date) / 1000
                end_date = time.localtime(end_date)
                end_date = time.strftime("%Y-%m-%d 23:59:59", end_date)
                filter_dict['c_time__range'] = (start_date, end_date)
        except:
            data = {'code': '999999', 'msg': '时间错误'}
            return JsonResponse(data)
        if channel_type:
            user = UserAdmin.objects.filter(channel_type=channel_type).order_by('username')
        else:
            user = UserAdmin.objects.all().order_by('username')

        if trade_type:
            filter_dict['trade_type'] = trade_type

        items = user.values()
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

        items = []
        data = {}
        all_money = 0
        all_order_count = 0
        all_channel = set()

        for each in res:
            item = {}
            username = each['username']
            nick_name = each['ymt_name']
            filter_dict['username'] = username
            model = OrderList.objects.filter(**filter_dict).all()

            order_count = model.count()
            all_order_count = all_order_count + order_count

            total_money = model.aggregate(total_money=Sum('pay_money'))
            total_money = total_money['total_money']
            if total_money:
                total_money = round(total_money, 2)
            else:
                total_money = 0
            all_money = all_money + total_money
            item['username'] = username
            item['nick_name'] = nick_name
            channel_type = each['channel_type']
            item['channel_type'] = channel_type
            if channel_type:
                all_channel.update([channel_type, ])
            if trade_type:
                item['trade_type'] = trade_type
            else:
                item['trade_type'] = '全部'
            item['order_count'] = order_count
            item['total_money'] = total_money
            items.append(item)
            print(username, nick_name, order_count, total_money)
        print(all_channel)
        data['code'] = '000000'
        data['data'] = items
        data['count'] = count
        data['total_page'] = total_page
        data['all_money'] = all_money
        data['all_order_count'] = all_order_count
        data['channel_count'] = len(all_channel)
        return JsonResponse(data)


class PaymentViewsets(viewsets.GenericViewSet):
    serializer_class = PaymentSerializer

    def create(self, request):
        username = request.data.get('username', None)
        page = request.data.get('page', '1')
        page_size = request.data.get('page_size', '15')
        start_date = request.data.get('start_date', None)
        try:
            if start_date:
                start_date = int(start_date) / 1000
                start_date = time.localtime(start_date)
                start_date = time.strftime("%Y-%m-%d %H:%M:%S", start_date)

            end_date = request.data.get('end_date', None)
            if end_date:
                end_date = int(end_date) / 1000
                end_date = time.localtime(end_date)
                end_date = time.strftime("%Y-%m-%d %H:%M:%S", end_date)
        except:
            data = {'code': '999999', 'msg': '时间错误'}
            return JsonResponse(data)
        wx = UserAdmin.objects.filter(username=username).first()

        # 没有username 情况 返回全部
        if wx:
            channel_type = wx.channel_type
            if channel_type == 'UL':
                filter_dict = {}

                try:
                    if username:
                        filter_dict['username'] = username
                    if start_date and end_date:
                        filter_dict['end_date__range'] = (start_date, end_date)
                except:
                    pass
                model = paymentList.objects.filter(**filter_dict).order_by('-end_date')
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
                total_money = model.aggregate(total_money=Sum('trade_money'))
                charge_total_money = model.aggregate(charge_total_money=Sum('charge'))
                total_money = total_money['total_money']
                charge_total_money = charge_total_money['charge_total_money']
                data = {}
                data['code'] = '000000'
                data['data'] = res
                data['total_page'] = total_page
                data['count'] = count
                # 总计
                if total_money:
                    try:
                        data['total_money'] = round(float(total_money), 2)
                    except:
                        data['total_money'] = round(total_money, 2)
                else:
                    data['total_money'] = total_money
                # 余额
                if charge_total_money:
                    try:
                        data['charge_total_money'] = round(float(charge_total_money), 2)
                    except:
                        data['charge_total_money'] = round(charge_total_money, 2)
                else:
                    data['charge_total_money'] = charge_total_money

                return JsonResponse(data)
        else:
            data = {'code': '576757', 'msg': '账号错误'}
            return JsonResponse(data)
