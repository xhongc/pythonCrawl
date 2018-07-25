from rest_framework import serializers
from qmf_api.models import OrderList


class QmforderSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, help_text='username')
    page = serializers.IntegerField(required=False, help_text='查询页数')
    trade_type = serializers.CharField(required=False, help_text='支付类型 支付宝, 微信')
    switch = serializers.CharField(required=False, help_text='备注开关 1为开')
    start_date = serializers.CharField(required=False, help_text='2018-07-10')
    end_date = serializers.CharField(required=False, help_text='2018-07-10')
    serach_type = serializers.CharField(required=False, help_text='查询类型')
    page_size = serializers.CharField(required=False, help_text='当页条数')


class GCodeSerializer(serializers.Serializer):
    productName = serializers.CharField(help_text='商品名称')
    productAmout = serializers.CharField(help_text='商品金额')
    productId = serializers.CharField(help_text='商品备注')


class UpOrderSerializer(serializers.Serializer):
    PayNO = serializers.CharField(required=True, min_length=27, max_length=27, help_text='订单号27位')
    PayJe = serializers.CharField(required=True, help_text='交易金额')
    payType = serializers.CharField(required=True, help_text='1为支付宝，2为微信')
    PayMore = serializers.CharField(required=True, help_text='二维码备注 exp：327-100-03')


class AddOrderSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, help_text='用户名称')
    c_time = serializers.CharField(required=False, help_text='时间')
    order_no = serializers.CharField(required=False, help_text='订单')
    pay_money = serializers.CharField(required=False, help_text='金额')
    trade_type = serializers.CharField(required=False, help_text='支付类型')
    trade_status = serializers.CharField(required=False, help_text='支付类型', default='成功')
    beizhu = serializers.CharField(required=False, help_text='商品备注')
    beizhu2 = serializers.CharField(required=False, help_text='二维码备注')

    class Meta:
        model = OrderList
        fields = (
            'username', 'c_time', 'order_no', 'pay_money', 'trade_type', 'trade_status', 'beizhu', 'beizhu2', 'beizhu2')
