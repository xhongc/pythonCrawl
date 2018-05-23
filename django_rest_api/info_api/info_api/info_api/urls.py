from rest_framework.documentation import include_docs_urls
from django.conf.urls import url,include
from django.contrib import admin
from people.views import PeopleViewset
from rest_framework.routers import DefaultRouter
from people.views import Total_Count
router = DefaultRouter()
router.register(r'users', PeopleViewset, base_name='users')
router.register(r'total', Total_Count, base_name='total')
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^', include(router.urls)),
    url(r'^docs/',include_docs_urls(title='API', description='young api')),
    #url(r'^total/',Total_Count.as_view())

]
