from django.contrib import admin
from qmf_api.models import Wxsession,OrderList
import xadmin
# Register your models here.


xadmin.site.register(Wxsession)
xadmin.site.register(OrderList)
