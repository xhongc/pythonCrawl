from django.db import models


# Create your models here.
class Wxsession(models.Model):
    wx_session = models.CharField('wx_session', max_length=65, blank=True, null=True)

    class Meta:
        verbose_name = "微信授权"
        verbose_name_plural = verbose_name


class OrderList(models.Model):
    c_time = models.CharField('时间', max_length=255, blank=True, null=True)
    order_no = models.CharField('dingdan', max_length=255, blank=True, null=True)
    pay_money = models.CharField('pay_money', max_length=255, blank=True, null=True)
    trade_type = models.CharField('trade_type', max_length=255, blank=True, null=True)
    trade_status = models.CharField('trade_status', max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "订单详情"
        verbose_name_plural = verbose_name
