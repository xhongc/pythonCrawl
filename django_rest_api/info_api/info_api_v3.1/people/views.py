from django.shortcuts import render
from .serializers import PeopleSeriazars, JoinTimeSeriazers, CheckSerilizars, LoginSerilizars, BankSerilizars
from .serializers import HistorySerilizars, UserSearchSerilizars
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework import mixins
from .models import People, Join_time, BankInfo, History
from rest_framework.views import APIView
from django.db.models import Count, Sum
import json
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from datetime import datetime


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


class PeopleViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
    list:
        用户列表，分页
    retrieve:
        获取用户详情
    create:
        添加用户名，金额
    '''

    # 这里必须要定义一个默认的排序,否则会报错
    queryset = People.objects.all().order_by('id')
    # 分页
    pagination_class = GoodsPagination
    # 序列化
    serializer_class = PeopleSeriazars


# class Total_Count(APIView, mixins.CreateModelMixin):
#     """
#     返回总人数 ，总金额
#
#     """
#
#     def get(self, requset):
#         total_money = People.objects.aggregate(total_money=Sum('money'))
#         people_list = People.objects.values('username').distinct()  # ClassName.objects.values('name').distinct()
#         total_money['people_num'] = len(people_list)
#         # print(total_money)
#         return JsonResponse(total_money)
class Total_Count(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''
    list:
        返回总人数 ，总金额

    '''
    queryset = People.objects.all().order_by('id')
    serializer_class = PeopleSeriazars

    def list(self, requset):
        total_money = People.objects.aggregate(total_money=Sum('money'))
        people_list = People.objects.values('username').distinct()  # ClassName.objects.values('name').distinct()
        total_money['people_num'] = round(len(people_list), 2)
        # print(total_money)
        return JsonResponse(total_money)


class JoinViewsets(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    list:
        显示活动详情
    create:
        添加用户 ， 选择参与时长
    update:
        更改状态
    """
    pagination_class = GoodsPagination
    queryset = Join_time.objects.all().order_by('id')
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (BasicAuthentication, SessionAuthentication)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('=id',)


    def get_serializer_class(self):
        if self.action == "create":
            return JoinTimeSeriazers
        elif self.action == 'list':
            return JoinTimeSeriazers
        elif self.action == 'update':
            return CheckSerilizars
        else:
            return CheckSerilizars

    def perform_create(self, serializer):
        model = serializer.save()
        username_id = model.id
        add_time = model.add_time
        add_operation = u'参与了活动'
        new = History(username_id=username_id, add_time=add_time, add_operation=add_operation)
        new.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer, data=request.data)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer, data):
        model = serializer.save()
        username_id = model.id
        event_status = data.get('event_status', None)
        tixian_status = data.get('tixian_status', None)
        # print(event_status, tixian_status,data)
        new = History.objects.get(username_id=username_id)
        # new = History(username_id=username_id, update_time=update_time)
        if new:
            if event_status == 1:
                update_time = datetime.now()
                new.update_operation = u'修改状态为成功'
                new.update_time = update_time
                new.save()
            elif event_status == 2:
                update_time = datetime.now()
                new.update_operation = u'修改状态为失败'
                new.update_time = update_time
                new.save()

            if tixian_status == 1:
                tixian_time = datetime.now()
                new.tixian_operation = u'已领取奖金'
                new.tixian_time = tixian_time
                new.save()
            elif tixian_status == 0:
                tixian_time = datetime.now()
                new.tixian_operation = u'未领取奖金'
                new.tixian_time = tixian_time
                new.save()


class LoginViewsets(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    create:
        登陆
    """
    queryset = User.objects.all().order_by('id')
    serializer_class = LoginSerilizars

    def create(self, request, *args, **kwargs):
        pass_word = request.data.get('password', None)
        # print('pass               ',pass_word,request.data)
        user = authenticate(username='admin', password=pass_word)
        if user is not None:
            if user.is_active:
                login(request, user)

                return JsonResponse({'code': '1', 'msg': '登陆成功'})
        return JsonResponse({'code': '0', 'msg': '登陆失败'})


class BankViewsets(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    create:
        添加银行卡
    """

    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('=username',)

    queryset = BankInfo.objects.all().order_by('id')
    serializer_class = BankSerilizars


class HistoryViewsets(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    retrieve:
        历史记录
    """
    queryset = History.objects.all().order_by('id')
    serializer_class = HistorySerilizars

    def create(self, request, *args, **kwargs):
        username = request.data.get('username', None)
        item = {}
        if username:
            model = History.objects.filter(username=username)
            try:
                item['add_time'] = model[0].add_time.strftime('%Y-%m-%d %H:%M')
                item['add_operation'] = model[0].add_operation
            except:
                pass
            try:
                item['update_time'] = model[0].update_time.strftime('%Y-%m-%d %H:%M')
                item['update_operation'] = model[0].update_operation
            except:
                pass
            try:
                item['tixian_time'] = model[0].tixian_time.strftime('%Y-%m-%d %H:%M')
                item['tixian_operation'] = model[0].tixian_operation
            except:
                pass

        return JsonResponse(item)


class UserSearchViewsets(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Join_time.objects.all().order_by('id')
    serializer_class = UserSearchSerilizars

    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('=username',)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)



