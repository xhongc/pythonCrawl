from rest_framework import serializers
from qmf_api.models import OrderList


class QmforderSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, help_text='username')
    page = serializers.IntegerField(required=False, help_text='查询页数')
    page_size = serializers.CharField(required=False, help_text='当页条数')
    trade_type = serializers.CharField(required=False, help_text='支付类型 支付宝, 微信')
    account_status = serializers.CharField(required=False, help_text='结算状态')
    switch = serializers.CharField(required=False, help_text='备注开关 1为开')
    start_date = serializers.CharField(required=False, help_text='2018-07-10')
    end_date = serializers.CharField(required=False, help_text='2018-07-10')
    serach_type = serializers.CharField(required=False, help_text='查询类型')


class GCodeSerializer(serializers.Serializer):
    login = serializers.CharField(required=False, help_text='账号')
    productName = serializers.CharField(help_text='商品名称')
    productAmout = serializers.CharField(help_text='商品金额')
    productId = serializers.CharField(required=False, help_text='商品备注')


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


class StatisticsSerializer(serializers.Serializer):
    page = serializers.IntegerField(label='page', required=False, help_text='查询页数')
    page_size = serializers.CharField(label='page_size', required=False, help_text='当页条数')
    username = serializers.CharField(label='用户名', required=False, read_only=True)
    nicke_name = serializers.CharField(label='昵称', required=False, read_only=True)
    channel_type = serializers.CharField(label='平台', required=False, help_text='YL,KQ')
    trade_type = serializers.CharField(label='支付方式', required=False)
    order_count = serializers.CharField(label='总笔数', required=False, read_only=True)
    total_money = serializers.CharField(label='总金额', required=False, read_only=True)
    start_date = serializers.CharField(label='开始时间', required=False, help_text='1534495819000')
    end_date = serializers.CharField(label='结束时间', required=False, help_text='1534495819000')


class PaymentSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, help_text='username')
    page = serializers.IntegerField(required=False, help_text='查询页数')
    page_size = serializers.CharField(required=False, help_text='当页条数')
    start_date = serializers.CharField(required=False, help_text='2018-07-10')
    end_date = serializers.CharField(required=False, help_text='2018-07-10')
