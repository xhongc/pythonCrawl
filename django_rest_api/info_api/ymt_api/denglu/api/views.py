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
from django.middleware.csrf import get_token ,rotate_token

# 分页类，重写get_paginated_response 加入总页数
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


# 订单详情，调用tools 里爬虫方法
class OrderViewset(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取订单详情
    create:
        根据交易类型页数查询
    """
    serializer_class = OrderSerializer
    authentication_classes = (BasicAuthentication,)

    def list(self, request):
        # print(request.user.ymt_name)
        try:
            cookies = request.session.get('cookies', None)
            if not cookies:
                # 登陆后 保存username 提取moedel 相应一码通账号密码
                username = request.session.get('username')
                model = UserAdmin.objects.filter(username=username).first()
                ymt_name = model.ymt_name
                ymt_pwd = model.ymt_pwd

                cookies = get_cookies(ymt_name, ymt_pwd)
                request.session['cookies'] = cookies
            cookies = request.session['cookies']
            data = get_order(cookies)
        except KeyError:
            username = request.session.get('username')
            model = UserAdmin.objects.filter(username=username).first()
            ymt_name = model.ymt_name
            ymt_pwd = model.ymt_pwd
            cookies = get_cookies(ymt_name, ymt_pwd)

            request.session['cookies'] = cookies

            try:
                data = get_order(cookies)
            except TypeError:
                data = {'code': '1', 'msg': u'无数据·'}
            except KeyError:
                data = {'code': '2', 'msg': u'出现未知问题'}
        except TypeError:
            data = {'code': '1', 'msg': u'无数据·1'}
        return JsonResponse(data)

    def create(self, request, *args, **kwargs):
        # 参数查询
        trade_type = request.data.get('trade_type', 0)
        page = request.data.get('page', 1)

        try:
            if not request.session['cookies']:
                username = request.session.get('username')
                model = UserAdmin.objects.filter(username=username).first()
                ymt_name = model.ymt_name
                ymt_pwd = model.ymt_pwd
                cookies = get_cookies(ymt_name, ymt_pwd)

                request.session['cookies'] = cookies
            cookies = request.session['cookies']
            data = get_order(cookies, trade_type, page)
        except KeyError:
            username = request.session.get('username')
            model = UserAdmin.objects.filter(username=username).first()
            ymt_name = model.ymt_name
            ymt_pwd = model.ymt_pwd
            cookies = get_cookies(ymt_name, ymt_pwd)

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


class DayOrderViewset(viewsets.GenericViewSet):
    """
        list:
            日统计
    """
    serializer_class = OrderSerializer
    # permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,)

    def list(self, request):

        try:
            if not request.session['cookies']:
                username = request.session.get('username')
                model = UserAdmin.objects.filter(username=username).first()
                ymt_name = model.ymt_name
                ymt_pwd = model.ymt_pwd
                cookies = get_cookies(ymt_name, ymt_pwd)

                request.session['cookies'] = cookies
            cookies = request.session['cookies']
            data = get_dayorder(cookies)
        except KeyError:
            username = request.session.get('username')
            model = UserAdmin.objects.filter(username=username).first()
            ymt_name = model.ymt_name
            ymt_pwd = model.ymt_pwd
            cookies = get_cookies(ymt_name, ymt_pwd)

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

        if str(search_type) == '0':
            try:
                if not request.session['cookies']:
                    username = request.session.get('username')
                    model = UserAdmin.objects.filter(username=username).first()
                    ymt_name = model.ymt_name
                    ymt_pwd = model.ymt_pwd
                    cookies = get_cookies(ymt_name, ymt_pwd)

                    request.session['cookies'] = cookies
                cookies = request.session['cookies']
                data = get_dayorder(cookies, trade_type)
            except KeyError:
                username = request.session.get('username')
                model = UserAdmin.objects.filter(username=username).first()
                ymt_name = model.ymt_name
                ymt_pwd = model.ymt_pwd
                cookies = get_cookies(ymt_name, ymt_pwd)

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
                    username = request.session.get('username')
                    model = UserAdmin.objects.filter(username=username).first()
                    ymt_name = model.ymt_name
                    ymt_pwd = model.ymt_pwd
                    cookies = get_cookies(ymt_name, ymt_pwd)

                    request.session['cookies'] = cookies
                cookies = request.session['cookies']
                data = get_monthorder(cookies, trade_type)
            except KeyError:
                username = request.session.get('username')
                model = UserAdmin.objects.filter(username=username).first()
                ymt_name = model.ymt_name
                ymt_pwd = model.ymt_pwd
                cookies = get_cookies(ymt_name, ymt_pwd)

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


class LoginViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    create:
        登陆
    """
    queryset = UserAdmin.objects.all().order_by('id')
    serializer_class = LoginSerializer

    def list(self, request):
        token = get_token(request)
        return JsonResponse({'token': token})

    def create(self, request, *args, **kwargs):
        user_name = request.data.get('username', None)
        user_pwd = request.data.get('password', None)
        # 因前端不传 CSRF 故authenticate，login内置方法无法正常使用
        user = authenticate(username=user_name, password=user_pwd)
        # user = UserAdmin.objects.filter(username=user_name).first()
        request_csrf_token = request.POST.get('csrfmiddlewaretoken', '')
        print(request_csrf_token)
        if user is not None:
            print('<%s>:<%s>' % (user, user_pwd))
            if user.display_password == user_pwd:
                print('<%s>:<%s>' % (user, user_pwd))
                if str(user.is_status) == '1':
                    login(request, user)
                    # 登陆后 将username保存全局中
                    request.session['username'] = user_name

                    # 获取访问者IP
                    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                    if x_forwarded_for:
                        ip = x_forwarded_for.split(',')[0]
                    else:
                        ip = request.META.get('REMOTE_ADDR')

                    # last登陆时间
                    model = UserAdmin.objects.filter(username=user_name).first()
                    model.login_ip = ip
                    model.last_login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    model.save()
                    # 超级用户判断
                    if user.is_superuser:
                        return JsonResponse({'code': '100', 'msg': '登陆成功'})
                    else:
                        return JsonResponse({'code': '101', 'msg': '登陆成功'})
        return JsonResponse({'code': '0', 'msg': '登陆失败'})


class UserViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    create:
        用户修改密码（登陆状态下）
    """
    serializer_class = UserUpdateSerializer
    queryset = UserAdmin.objects.all().order_by('id')
    authentication_classes = (BasicAuthentication,)

    def create(self, request, *args, **kwargs):
        username = request.session.get('username', None)
        old_password = request.data.get('old_password', None)
        if username:
            user = UserAdmin.objects.filter(username=username).first()
            # print(dir(user))
            if user.password != old_password:
                return Response({'code': 1, 'msg': '旧密码不正确'}, status=status.HTTP_400_BAD_REQUEST)
            if request.data.get('password2') != request.data.get('password'):
                return Response({'code': 1, 'msg': '两次密码不一样'}, status=status.HTTP_400_BAD_REQUEST)

            new_pwd = request.data.get('password')

            user = UserAdmin.objects.filter(username=username).first()
            user.password = new_pwd
            user.display_password = request.data.get('password')
            user.save()

            return Response({'code': 1, 'msg': '成功a'}, status=status.HTTP_201_CREATED)
        return Response({'code': 0, 'msg': '000'}, status=status.HTTP_201_CREATED)


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

    queryset = UserAdmin.objects.all().order_by('id')
    authentication_classes = (BasicAuthentication,)
    pagination_class = GoodsPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('$username',)

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
        # copy 一份data ，原有不能修改，之前加密时需要
        new_data = request.data.copy()
        new_pwd = request.data.get('password')
        new_data['password'] = new_pwd
        new_data['display_password'] = request.data.get('password')
        serializer = UserSerializer(data=new_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        new_data = request.data.copy()
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        pass1 = request.data.get('password', None)
        if pass1 is not None:
            new_pwd = request.data.get('password', None)
            if new_pwd:
                new_data['display_password'] = pass1

        serializer = self.get_serializer(instance, data=new_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class RandomPWD(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
        list:
            随机密码（just for fun）
    """
    serializer_class = OrderSerializer

    def list(self, request, *args, **kwargs):
        randompwd = random.randint(100000, 999999)
        data = {'randompwd': randompwd}
        return JsonResponse(data)


class PeaceBankOrderViewsets(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = OrderSerializer

    def list(self, request):
        try:
            # username = request.session.get('username')
            # model = UserAdmin.objects.filter(username=username).first()
            # peace_name = model.ymt_name
            # peace_pwd = model.ymt_pwd
            peace_name = '530580007822'
            peace_pwd = 'qq360360'
            peace = PeaceBank(peace_name, peace_pwd)
            data = peace.run()

        except:
            data = {'code': '1', 'msg': u' 未登陆'}

        # print(data)
        return JsonResponse(data)

    def create(self, request):
        try:
            username = request.session.get('username')
            model = UserAdmin.objects.filter(username=username).first()
            peace_name = model.ymt_name
            peace_pwd = model.ymt_pwd
            # peace_name = '530580007822'
            # peace_pwd = 'qq360360'
            peace = PeaceBank(peace_name, peace_pwd)
            data = peace.getOrder()

        except:
            data = {'code': '1', 'msg': u' 未登陆'}

        # print(data)
        return JsonResponse(data)
