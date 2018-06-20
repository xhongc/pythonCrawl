from rest_framework import serializers
from api.models import UserAdmin


class OrderSerializer(serializers.Serializer):
    trade_type = serializers.IntegerField(required=False, help_text='支付类型 1为支付宝 2为微信支付')
    page = serializers.IntegerField(required=False, help_text='查询页数')
    search_type = serializers.CharField(required=False, help_text='类型 0为日 1为月')


class UserSerializer(serializers.ModelSerializer):
    display_password = serializers.CharField(required=False)

    class Meta:
        model = UserAdmin
        fields = ('username', 'password', 'display_password', 'url', 'ymt_name', 'ymt_pwd')


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAdmin
        fields = ('username', 'password')


class UserUpdateSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    class Meta:
        model = UserAdmin
        fields = ('old_password', 'password', 'password2')


class AdminUserSerializer(serializers.ModelSerializer):
    # id = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    url = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    display_password = serializers.CharField(read_only=True)
    ymt_name = serializers.CharField(required=False)
    ymt_pwd = serializers.CharField(required=False)
    is_status = serializers.IntegerField(label='启用状态', min_value=0,max_value=1,required=False,help_text='0关闭，1启用')
    login_ip = serializers.CharField(read_only=True)
    last_login_time = serializers.CharField(read_only=True)

    class Meta:
        model = UserAdmin
        fields = ('id', 'username', 'password', 'display_password','url', 'is_status', 'ymt_name', 'ymt_pwd', 'login_ip', 'last_login_time')
