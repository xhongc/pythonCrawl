from django.conf.urls import url, include
from django.urls import path, re_path
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from api.views import OrderViewset, LoginViewset, UserViewset, AdminUserViewset, DayOrderViewset, RandomPWD, \
    PeaceBankOrderViewsets
from qmf_api.views import QmfOrderViewsets, GenerateCodeViewsets, UpOrderViewsrts, AddOrderViewsets, StatisticsViewsets
from rest_framework.documentation import include_docs_urls
from django.views.generic import TemplateView
import xadmin

router = DefaultRouter()
# router.register(r'order', OrderViewset, base_name='order')
# router.register(r'order1', PeaceBankOrderViewsets, base_name='order1')
router.register(r'dayorder', DayOrderViewset, base_name='dayorder')
# router.register(r'monthorder', MonthOrderViewset, base_name='monthorder')
router.register(r'login', LoginViewset, base_name='login')
router.register(r'users', UserViewset, base_name='users')
router.register(r'adminuser', AdminUserViewset, base_name='adminuser')
router.register(r'RandomPWD', RandomPWD, base_name='RandomPWD')
router.register(r'qmf_order', QmfOrderViewsets, base_name='qmf_order')
router.register(r'gcode', GenerateCodeViewsets, base_name='gcode')
router.register(r'uporder', UpOrderViewsrts, base_name='uporder')
router.register(r'addorder', AddOrderViewsets, base_name='addorder')
router.register(r'statistics', StatisticsViewsets, base_name='statistics')

urlpatterns = [
    path('admin/', xadmin.site.urls),
    path('api/', include(router.urls)),
    path('docs/', include_docs_urls(title='API 与 狗', description='young api')),
    re_path('', TemplateView.as_view(template_name='index.html'), name='index'),

]
