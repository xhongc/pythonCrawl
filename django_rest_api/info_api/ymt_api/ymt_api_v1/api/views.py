from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from api.tools import get_cookies, get_order, get_dayorder, get_monthorder
from rest_framework import mixins
import json
from api.serializers import OrderSerializer
from rest_framework.response import Response
from api.serializers import UserSerializer, UserUpdateSerializer, AdminUserSerializer, LoginSerializer
from api.models import UserAdmin
from django.contrib.auth import login, authenticate
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
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


@method_decorator(csrf_exempt, name='dispatch')
class OrderViewset(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取订单详情
    create:
        根据交易类型页数查询
    """
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,)

    def list(self, request):
        # print(request.user.ymt_name)
        try:
            cookies = request.session.get('cookies',None)
            # print(cookies)
            if not cookies:
                cookies = get_cookies()
                request.session['cookies'] = cookies
            cookies = request.session['cookies']
            data = get_order(cookies)
        except KeyError:
            cookies = get_cookies()
            request.session['cookies'] = cookies
            try:
                data = get_order(cookies)
            except TypeError:
                data = {'code': '1', 'msg': u'无数据·'}
                # data = json.dumps(data, ensure_ascii=False)
            except KeyError:
                data = {'code': '2', 'msg': u'出现未知问题'}
                # data = json.dumps(data, ensure_ascii=False)
        except TypeError:
            data = {'code': '1', 'msg': u'无数据·1'}
            # data = json.dumps(data, ensure_ascii=False)
        return JsonResponse(data)

     
    def create(self, request, *args, **kwargs):
        trade_type = request.data.get('trade_type', 0)
        page = request.data.get('page', 1)

        try:
            if not request.session['cookies']:
                cookies = get_cookies()
                request.session['cookies'] = cookies
            cookies = request.session['cookies']
            data = get_order(cookies, trade_type, page)
        except KeyError:
            cookies = get_cookies()
            request.session['cookies'] = cookies
            try:
                data = get_order(cookies, trade_type, page)
            except TypeError as e:
                # print(e)
                data = {'code': '1', 'msg': u'无数据·'}
                # data = json.dumps(data, ensure_ascii=False)
            except KeyError:
                data = {'code': '2', 'msg': u'出现未知问题'}
                # data = json.dumps(data, ensure_ascii=False)
        except TypeError:
            data = {'code': '1', 'msg': u'无数据·1'}
            # data = json.dumps(data, ensure_ascii=False)
        # print(data)
        return JsonResponse(data)

@method_decorator(csrf_exempt, name='dispatch')
class DayOrderViewset(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
        list:
            日统计
    """
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,)

    def list(self, request):
        # print(request.user.ymt_name)
        try:
            if not request.session['cookies']:
                cookies = get_cookies()
                request.session['cookies'] = cookies
            cookies = request.session['cookies']
            data = get_dayorder(cookies)
        except KeyError:
            cookies = get_cookies()
            request.session['cookies'] = cookies
            try:
                data = get_dayorder(cookies)
            except TypeError:
                data = {'code': '1', 'msg': u'无数据·'}
                # data = json.dumps(data, ensure_ascii=False)
            except KeyError:
                data = {'code': '2', 'msg': u'出现未知问题'}
                # data = json.dumps(data, ensure_ascii=False)
        except TypeError:
            data = {'code': '1', 'msg': u'无数据·1'}
            # data = json.dumps(data, ensure_ascii=False)
        return JsonResponse(data)

     
    def create(self, request, *args, **kwargs):
        trade_type = request.data.get('trade_type', 0)
        search_type = request.data.get('search_type', '0')
        # print(type(search_type),search_type)
        if str(search_type) == '0':
            try:
                if not request.session['cookies']:
                    cookies = get_cookies()
                    request.session['cookies'] = cookies
                cookies = request.session['cookies']
                data = get_dayorder(cookies, trade_type)
            except KeyError:
                cookies = get_cookies()
                request.session['cookies'] = cookies
                try:
                    data = get_dayorder(cookies, trade_type)
                except TypeError:
                    data = {'code': '1', 'msg': u'无数据·'}
                    # data = json.dumps(data, ensure_ascii=False)
                except KeyError:
                    data = {'code': '2', 'msg': u'出现未知问题'}
                    # data = json.dumps(data, ensure_ascii=False)
            except TypeError:
                data = {'code': '1', 'msg': u'无数据·1'}
                # data = json.dumps(data, ensure_ascii=False)
            return JsonResponse(data)
        elif str(search_type) == '1':
            try:
                # print('aaaa')
                if not request.session['cookies']:
                    cookies = get_cookies()
                    request.session['cookies'] = cookies
                cookies = request.session['cookies']
                data = get_monthorder(cookies, trade_type)
            except KeyError:
                cookies = get_cookies()
                request.session['cookies'] = cookies
                try:
                    data = get_monthorder(cookies, trade_type)
                except TypeError:
                    data = {'code': '1', 'msg': u'无数据·'}
                    # data = json.dumps(data, ensure_ascii=False)
                except KeyError:
                    data = {'code': '2', 'msg': u'出现未知问题'}
                    # data = json.dumps(data, ensure_ascii=False)
            except TypeError:
                data = {'code': '1', 'msg': u'无数据·1'}
                # data = json.dumps(data, ensure_ascii=False)
            return JsonResponse(data)
        else:
            return JsonResponse({'code': '2', 'msg': u'出现未知问题'})

@method_decorator(csrf_exempt, name='dispatch')
class MonthOrderViewset(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    list:
        月统计
    """
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,)

    def list(self, request):
        # print(request.user.ymt_name)
        try:
            if not request.session['cookies']:
                cookies = get_cookies()
                request.session['cookies'] = cookies
            cookies = request.session['cookies']
            data = get_monthorder(cookies)
        except KeyError:
            cookies = get_cookies()
            request.session['cookies'] = cookies
            try:
                data = get_monthorder(cookies)
            except TypeError:
                data = {'code': '1', 'msg': u'无数据·'}
                # data = json.dumps(data, ensure_ascii=False)
            except KeyError:
                data = {'code': '2', 'msg': u'出现未知问题'}
                # data = json.dumps(data, ensure_ascii=False)
        except TypeError:
            data = {'code': '1', 'msg': u'无数据·1'}
            # data = json.dumps(data, ensure_ascii=False)
        return JsonResponse(data)

     
    def create(self, request, *args, **kwargs):
        trade_type = request.data.get('trade_type', 0)
        try:
            if not request.session['cookies']:
                cookies = get_cookies()
                request.session['cookies'] = cookies
            cookies = request.session['cookies']
            data = get_monthorder(cookies, trade_type)
        except KeyError:
            cookies = get_cookies()
            request.session['cookies'] = cookies
            try:
                data = get_monthorder(cookies, trade_type)
            except TypeError:
                data = {'code': '1', 'msg': u'无数据·'}
                # data = json.dumps(data, ensure_ascii=False)
            except KeyError:
                data = {'code': '2', 'msg': u'出现未知问题'}
                # data = json.dumps(data, ensure_ascii=False)
        except TypeError:
            data = {'code': '1', 'msg': u'无数据·1'}
            # data = json.dumps(data, ensure_ascii=False)
        return JsonResponse(data)

@method_decorator(csrf_exempt, name='dispatch')
class LoginViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    create:
        登陆
    """
    queryset = UserAdmin.objects.all().order_by('id')
    serializer_class = LoginSerializer

     
    def create(self, request, *args, **kwargs):
        user_name = request.data.get('username', None)
        user_pwd = request.data.get('password', None)

        user = authenticate(username=user_name, password=user_pwd)
        print(user_name,user_pwd,user)
        if user is not None:
            print(user.is_active)
            if user.is_active:
                login(request, user)

                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')

                model = UserAdmin.objects.filter(username=user_name).first()
                model.login_ip = ip
                model.last_login_time = datetime.now()
                # print(ip,datetime.now())
                model.save()
                if user.is_superuser:
                    return JsonResponse({'code': '100', 'msg': '登陆成功'})
                else:
                    return JsonResponse({'code': '101', 'msg': '登陆成功'})
        return JsonResponse({'code': '0', 'msg': '登陆失败'})

@method_decorator(csrf_exempt, name='dispatch')
class UserViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    create:
        用户修改密码（登陆状态下）
    """
    serializer_class = UserUpdateSerializer
    queryset = UserAdmin.objects.all().order_by('id')
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,)

    # def get_serializer_class(self):
    #     if self.action == 'create':
    #         return UserSerializer
    #     elif self.action == 'update':
    #         return UserUpdateSerializer
    #     return UserSerializer
     
    def create(self, request, *args, **kwargs):
        if request.data.get('password2') != request.data.get('password'):
            return Response({'code': 1, 'msg': '两次密码不一样'}, status=status.HTTP_400_BAD_REQUEST)

        # jiami
        new_pwd = make_password(request.data.get('password'))
        user = UserAdmin.objects.filter(username=request.user.username).first()
        user.password = new_pwd
        user.save()

        return Response({'code': 1, 'msg': '成功a'}, status=status.HTTP_201_CREATED)

# @method_decorator(csrf_exempt, name='dispatch')
class AdminUserViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):
    """
    list:
        后台账号管理
    create:
        创建账号s
    update:
        账号修改
    """
    # serializer_class = AdminUserSerializer
    queryset = UserAdmin.objects.all().order_by('id')
    authentication_classes = (BasicAuthentication,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('=username',)
    # def get_permissions(self):
    #     if self.action == 'create':
    #         return [IsAuthenticated(),]
    #     return [IsAuthenticated(), ]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserSerializer
        elif self.action == 'update':
            return AdminUserSerializer
        return AdminUserSerializer

     
    def create(self, request, *args, **kwargs):
        new_data = request.data.copy()
        new_pwd = make_password(request.data.get('password'))
        new_data['password'] = new_pwd
        new_data['display_password'] = request.data.get('password')
        # print(new_data)
        serializer = UserSerializer(data=new_data)
        serializer.is_valid(raise_exception=True)
        #print(serializer)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        # jiami
        new_data = request.data.copy()
        new_pwd = make_password(request.data.get('password',None))
        if new_pwd:
            new_data['password'] = new_pwd

        serializer = self.get_serializer(instance, data=new_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
