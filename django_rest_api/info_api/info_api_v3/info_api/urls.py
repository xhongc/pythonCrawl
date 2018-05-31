from rest_framework.documentation import include_docs_urls
from django.conf.urls import url, include
from django.contrib import admin
from people.views import PeopleViewset, JoinViewsets, LoginViewsets, BankViewsets, HistoryViewsets, UserSearchViewsets
from rest_framework.routers import DefaultRouter
from people.views import Total_Count
from django.views.generic import TemplateView

router = DefaultRouter()
router.register(r'users', PeopleViewset, base_name='users')
router.register(r'total', Total_Count, base_name='total')
router.register(r'event', JoinViewsets, base_name='event')
router.register(r'login', LoginViewsets, base_name='login')
router.register(r'bankinfo', BankViewsets, base_name='bankinfo')
router.register(r'history', HistoryViewsets, base_name='history')
router.register(r'usersearch', UserSearchViewsets, base_name='usersearch')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^', include(router.urls)),
    url(r'^docs/', include_docs_urls(title='API & Dog', description='young api')),
    url(r'^index', TemplateView.as_view(template_name="caipiaoIndex.html")),
    # url(r'login/',LoginView.as_view())
    # url(r'^api-auth/', include('rest_framework.urls')),
]
