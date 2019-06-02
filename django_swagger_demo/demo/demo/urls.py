from django.conf.urls import url, include
from rest_framework_swagger.views import get_swagger_view

# schema_view = get_swagger_view(title='Demo Swagger API')
# from .swagger_schema import SwaggerSchemaView
#
# urlpatterns = [
#     url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
#     url(r'^cbv/', include('cbv_demo.urls')),
#     url(r'^fbv/', include('fbv_demo.urls')),
#     url(r'^swagger/', SwaggerSchemaView.as_view()),
# ]

from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from cbv_demo import views

# 路由
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, base_name='user')
router.register(r'groups', views.GroupViewSet, base_name='group')

# 重要的是如下三行
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

schema_view = get_schema_view(title='Users API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

urlpatterns = [
    # swagger接口文档路由
    url(r'^docs/', schema_view, name="docs"),
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    # drf登录
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]
