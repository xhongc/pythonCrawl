from rest_framework import serializers

from api.models import UserAdmin, UserBelong


# 订单序列化
class OrderSerializer(serializers.Serializer):
    trade_type = serializers.IntegerField(required=False, help_text='支付类型 1为支付宝 2为微信支付')
    page = serializers.IntegerField(required=False, help_text='查询页数')
    search_type = serializers.CharField(required=False, help_text='类型 0为日 1为月')


# 用户操作
class UserSerializer(serializers.ModelSerializer):
    display_password = serializers.CharField(required=False)

    class Meta:
        model = UserAdmin
        fields = ('username', 'password', 'display_password', 'url', 'ymt_name', 'ymt_pwd', 'channel_type')


# 登陆
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAdmin
        fields = ('username', 'password')


# 用户更新
class UserUpdateSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    class Meta:
        model = UserAdmin
        fields = ('old_password', 'password', 'password2')


class UserAttrSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    user = serializers.CharField(read_only=True)
    belong = serializers.CharField(read_only=True)
    connect_status = serializers.CharField(read_only=True)
    cookie = serializers.CharField(read_only=True)

    class Meta:
        model = UserBelong
        fields = '__all__'


class UserBelongSerializers(serializers.ModelSerializer):
    # user = serializers.CharField(required=False)
    user = serializers.PrimaryKeyRelatedField(required=True, queryset=UserAdmin.objects.all())
    # id = AdminUserSerializer(many=False)
    belong = serializers.CharField(required=False)
    connect_status = serializers.CharField(required=False)
    cookie = serializers.CharField(required=False)

    class Meta:
        model = UserBelong
        fields = ('belong', 'connect_status', 'cookie', 'user')


# 后台列表
class AdminUserSerializer(serializers.ModelSerializer):
    # id = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    belong_id = serializers.CharField(required=False)
    url = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    display_password = serializers.CharField(required=False)
    ymt_name = serializers.CharField(required=False)
    ymt_pwd = serializers.CharField(required=False)
    is_status = serializers.CharField(label='启用状态', required=False, help_text='0关闭，1启用', default='1')
    is_joke = serializers.CharField(label='用户权限', required=False, help_text='0关闭，1启用', default='1')
    login_ip = serializers.CharField(read_only=True)
    last_login_time = serializers.CharField(read_only=True)
    channel_type = serializers.CharField(required=False)
    # user = serializers.PrimaryKeyRelatedField(required=False, queryset=UserBelong.objects.all(), many=False)
    belong = serializers.CharField(label='belong', required=False)
    cookie = serializers.CharField(label='cookie', required=False)
    connect_status = serializers.CharField(label='connect_status', required=False)
    userbelong = serializers.SerializerMethodField(read_only=True)

    def get_userbelong(self, obj):
        user = UserAdmin.objects.get(id=obj.id)
        userbelong = user.userbelong.all().values()
        userbelong = list(userbelong)

        return userbelong

    # belong = UserAttrSerializer(many=True)

    class Meta:
        model = UserAdmin
        fields = (
            'id', 'belong_id', 'username', 'password', 'display_password', 'url', 'is_status', 'is_joke', 'ymt_name',
            'ymt_pwd',
            'login_ip', 'last_login_time', 'channel_type', 'belong', 'cookie', 'userbelong', 'connect_status')
