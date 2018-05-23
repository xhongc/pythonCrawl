from django.shortcuts import render
from .serializers import PeopleSeriazars
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework import mixins
from .models import People
from rest_framework.views import APIView
from django.db.models import Count, Sum
import json
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status


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


class PeopleViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
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
        total_money['people_num'] = len(people_list)
        # print(total_money)
        return JsonResponse(total_money)
