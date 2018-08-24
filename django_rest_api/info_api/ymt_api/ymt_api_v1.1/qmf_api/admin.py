from django.contrib import admin
from qmf_api.models import Wxsession, OrderList
import xadmin
from xadmin import views


# Register your models here.

class OrderListAdmin(object):
    list_display = ["c_time", "order_no", "pay_money", "trade_type", "beizhu", 'username']
    list_filter = ["trade_type", "c_time"]
    search_fields = ['username', 'order_no']


class BaseSetting(object):
    # 添加主题功能
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    # 全局配置，后台管理标题和页脚
    site_title = "后台 & Dog"
    site_footer = "Powered By a Handsome Man"
    # 菜单收缩
    menu_style = "accordion"


xadmin.site.register(Wxsession)
xadmin.site.register(OrderList, OrderListAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
