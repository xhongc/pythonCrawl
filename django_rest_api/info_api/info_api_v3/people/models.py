from django.db import models
from datetime import datetime


# Create your models here.
class People(models.Model):
    username = models.CharField('姓名', max_length=30, null=True, blank=True)
    money = models.CharField('金额', max_length=30, null=True, blank=True)


class Join_time(models.Model):
    time_type = (
        ('1', '1小时'),
        ('2', '2小时'),
        ('3', '3小时'),
        ('4', '4小时'),
        ('6', '6小时'),

    )
    status_check = (
        ('0', '审核中'),
        ('1', '成功'),
        ('2', '失败'),
    )
    username = models.CharField('姓名', max_length=30, null=True, blank=True)
    join_time = models.CharField('参与时长', max_length=3, choices=time_type)
    add_time = models.DateTimeField('添加时间', default=datetime.now)
    event_status = models.IntegerField('活动状态', default=0, null=True, blank=True, choices=status_check)
    # prize = models.IntegerField('奖金', null=True, blank=True)
    tixian_status = models.IntegerField('提现状态', default=0)
    reason = models.CharField('理由', max_length=255, null=True, blank=True)


class BankInfo(models.Model):
    username = models.ForeignKey(Join_time, max_length=30, null=True, blank=True)
    bankcard = models.CharField('银行卡号', max_length=19)
    name = models.CharField('姓名', max_length=10)
    bankaddr = models.CharField('开户行', max_length=30)
    phone_no = models.CharField('电话号码', max_length=11)


class History(models.Model):
    username = models.ForeignKey(Join_time, max_length=30, null=True, blank=True)
    add_time = models.DateTimeField('添加时间', null=True, blank=True)
    add_operation = models.CharField('添加操作', max_length=30, null=True, blank=True)
    update_time = models.DateTimeField('添加时间', null=True, blank=True)
    update_operation = models.CharField('添加操作', max_length=30, null=True, blank=True)
    tixian_time = models.DateTimeField('添加时间', null=True, blank=True)
    tixian_operation = models.CharField('添加操作', max_length=30, null=True, blank=True)
