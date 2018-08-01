from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.backends import ModelBackend
from .models import User, EmailVerifyRecord
from django.db.models import Q
from django.views.generic.base import View
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email


# def register(request):
#     redirect_to = request.POST.get('next',request.GET.get('next',''))
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#
#         if form.is_valid():
#             cur_user = form.save()
#             auth_login(request,cur_user)
#             if redirect_to:
#                 return redirect(redirect_to)
#             else:
#                 return redirect('/')
#     else:
#         form = RegisterForm()
#
#     return render(request,'users/register.html',context={'form':form})
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


def index(request):
    return render(request, 'index.html')


# def user_login(request):
#     if request.method == 'POST':
#         user_name = request.POST.get('username',None)
#         pass_word = request.POST.get('password',None)
#
#         user = authenticate(username=user_name,password=pass_word)
#         if user is not None:
#             login(request,user)
#             return render(request,'index.html')
#         else:
#             return render(request,'login.html',{'msg':'用户名或密码错误'})
#
#     elif request.method == 'GET':
#         return render(request,'login.html')
class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():

            user_name = request.POST.get('username', None)
            pass_word = request.POST.get('password', None)

            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})

        else:
            return render(request, 'login.html', {'login_form': login_form})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email')
            if User.objects.filter(email=user_name):
                return render(request, 'register.html', {'register': register_form}, {'msg': '用户已存在！'})
            pass_word = request.POST.get('password')
            user_profile = User()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()
            try:
                send_register_email(user_name, 'register')
            except BaseException as e:
                print('email out', e)
            return render(request, 'login.html')
        else:
            # form.is_valid（）已经判断不合法了，所以这里不需要再返回错误信息到前端了
            return render(request, 'register.html', {'register_form': register_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)

        if all_record:
            for record in all_record:
                email = record.email
                user = User.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html', {'msg': '你的激活链接无效'})
        return render(request, 'login.html')


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', None)
            send_register_email(email, send_type='forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "密码不一致！"})
            user = User.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})
