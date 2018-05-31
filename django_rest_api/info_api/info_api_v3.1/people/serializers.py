from rest_framework import serializers
from .models import People, Join_time, BankInfo, History
from datetime import datetime, timedelta
from django.contrib.auth.models import User


class PeopleSeriazars(serializers.ModelSerializer):
    username = serializers.CharField(required=True, label='用户名',
                                     error_messages={'required': '请输入用户名'})
    money = serializers.DecimalField(required=True, label='金额', max_digits=9, decimal_places=2,
                                     error_messages={'required': '请输入金额',
                                                     'decimal_places': '最大保留两位小数'})

    class Meta:
        model = People
        fields = "__all__"


class JoinTimeSeriazers(serializers.ModelSerializer):
    username = serializers.CharField(required=True, label='用户名',
                                     error_messages={'required': '请输入用户名'})

    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    prize = serializers.SerializerMethodField()
    event_status = serializers.IntegerField(read_only=True, help_text=u"<0审核中><1成功><2失败>")
    tixian_status = serializers.IntegerField(read_only=True)
    reason = serializers.CharField(read_only=True)

    def get_prize(self, obj):
        # print(obj)
        pri_map = {
            '1': '10',
            '2': '28',
            '3': '58',
            '4': '88',
            '6': '168',
        }
        index = obj.join_time
        # print(index)
        return pri_map[index]

    def validate_username(self, username):
        """
        验证是否已经参与活动
        """
        # 是否已经注册

        if Join_time.objects.filter(username=username).count():

            model = Join_time.objects.filter(username=username)
            model = model[0]
            hour = int(model.join_time)
            one_mintes_ago = datetime.now() - timedelta(hours=hour, minutes=0, seconds=0)
            if Join_time.objects.filter(add_time__gt=one_mintes_ago, username=username).count():
                raise serializers.ValidationError("已经参与，活动还在进行")

        return username

    class Meta:
        model = Join_time
        fields = "__all__"


class CheckSerilizars(serializers.ModelSerializer):
    event_status = serializers.IntegerField(required=False, label='审核状态', min_value=0, max_value=2)
    tixian_status = serializers.IntegerField(required=False, label='提现状态', min_value=0, max_value=1)
    reason = serializers.CharField(required=False, label='失败理由')

    class Meta:
        model = Join_time
        fields = ('event_status', 'tixian_status', 'reason')


class LoginSerilizars(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password',)


class BankSerilizars(serializers.ModelSerializer):
    username_id = serializers.IntegerField(required=True,help_text='用户的ID（数字）')
    bankcard = serializers.CharField(min_length=16)
    phone_no = serializers.CharField(min_length=11)

    class Meta:
        model = BankInfo
        fields = ('username_id','bankcard','phone_no','name','bankaddr')


class HistorySerilizars(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    update_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    tixian_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    add_operation = serializers.CharField(read_only=True)
    update_operation = serializers.CharField(read_only=True)
    tixian_operation = serializers.CharField(read_only=True)

    class Meta:
        model = History
        fields = "__all__"


class UserSearchSerilizars(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    class Meta:
        model = Join_time
        fields = ('id','username','join_time', 'add_time', 'event_status', 'reason')
