from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from api.views import OrderViewset, LoginViewset, UserViewset, AdminUserViewset, DayOrderViewset
from rest_framework.documentation import include_docs_urls
from django.views.generic import TemplateView

router = DefaultRouter()
router.register(r'order', OrderViewset, base_name='order')
router.register(r'dayorder', DayOrderViewset, base_name='dayorder')
# router.register(r'monthorder', MonthOrderViewset, base_name='monthorder')
router.register(r'login', LoginViewset, base_name='login')
router.register(r'users', UserViewset, base_name='users')
router.register(r'adminuser', AdminUserViewset, base_name='adminuser')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^api/', include(router.urls)),
    url('docs/', include_docs_urls(title='API 与 狗', description='young api')),
    url('index/', TemplateView.as_view(template_name='index.html'), name='index'),
]
