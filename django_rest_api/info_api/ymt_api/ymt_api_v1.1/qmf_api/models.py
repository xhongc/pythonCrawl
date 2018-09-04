from django.db import models


# Create your models here.
class Wxsession(models.Model):
    wx_session = models.CharField('wx_session', max_length=65, blank=True, null=True)

    class Meta:
        verbose_name = "微信授权"
        verbose_name_plural = verbose_name


# test1
class OrderList(models.Model):
    c_time = models.CharField('时间', max_length=255, blank=True, null=True)
    order_no = models.CharField('订单号', max_length=255, blank=True, null=True, unique=True)
    pay_money = models.CharField('金额', max_length=255, blank=True, null=True)
    charge = models.CharField('手续费', max_length=255, blank=True, null=True)
    trade_type = models.CharField('支付类型', max_length=255, blank=True, null=True)
    trade_status = models.CharField('支付状态', max_length=255, blank=True, null=True)
    account_status = models.CharField('结算状态', max_length=255, blank=True, null=True)
    username = models.CharField('username', max_length=255, blank=True, null=True)
    beizhu = models.CharField('beizhu', max_length=255, blank=True, null=True)
    beizhu2 = models.CharField('beizhu2', max_length=255, blank=True, null=True)
    belong = models.CharField('归属', max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "订单详情"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_no


class paymentList(models.Model):
    start_date = models.CharField('时间', max_length=255, blank=True, null=True)
    end_date = models.CharField('时间', max_length=255, blank=True, null=True)
    trade_no = models.CharField('订单号', max_length=255, blank=True, null=True, unique=True)
    withdraw_status = models.CharField('提现状态', max_length=255, blank=True, null=True)
    trade_money = models.CharField('金额', max_length=255, blank=True, null=True)
    charge = models.CharField('金额', max_length=255, blank=True, null=True)
    trade_status = models.CharField('支付状态', max_length=255, blank=True, null=True)
    username = models.CharField('username', max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "提现详情"
        verbose_name_plural = verbose_name
