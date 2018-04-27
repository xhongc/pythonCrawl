from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate
from django.contrib.auth.backends import ModelBackend
from .models import User
from django.db.models import Q
from django.views.generic.base import View
from .forms import LoginForm,RegisterForm
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_eamil


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
            user = User.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

def index(request):
    return render(request,'index.html')

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

    def get(self,request):
        return render(request,'login.html')

    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():

            user_name = request.POST.get('username',None)
            pass_word = request.POST.get('password', None)

            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                login(request,user)
                return render(request,'index.html')
            else:
                return render(request,'login.html',{'msg':'用户名或密码错误'})

        else:
            return render(request,'login.html',{'login_form':login_form})



class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request,'register.html',{'register_form':register_form})

    def post(self,request):
        register_form = RegisterForm()
        if register_form.is_valid():
            user_name = request.POST.get('email',None)
            if User.objects.filter(email=user_name):
                return render(request,'register.html',{'register':register_form},{'msg':'用户已存在！'})

            pass_word = request.POST.get('password',None)
            user_profile = User()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False

            user_profile.password = make_password(pass_word)
            user_profile.save()
            send_register_eamil(user_name,'register')
            return render(request,'login.html')

        # form.is_valid（）已经判断不合法了，所以这里不需要再返回错误信息到前端了
        else:
            return render(request,'register.html',{'register_form':register_form})
