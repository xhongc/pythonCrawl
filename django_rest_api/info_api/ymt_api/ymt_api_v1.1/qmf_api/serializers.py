from rest_framework import serializers


class QmforderSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, help_text='username')
    page = serializers.IntegerField(required=False, help_text='查询页数')
    trade_type = serializers.CharField(required=False, help_text='支付类型 Alipay 2.0为支付宝 WXPay为微信支付')
    switch = serializers.CharField(required=False, help_text='备注开关 1为开')
    billDate = serializers.CharField(required=False, help_text='2018-07-10')


class GCodeSerializer(serializers.Serializer):
    productName = serializers.CharField(help_text='商品名称')
    productAmout = serializers.CharField(help_text='商品金额')
    productId = serializers.CharField(help_text='商品备注')


class UpOrderSerializer(serializers.Serializer):
    PayNO = serializers.CharField(required=True, min_length=27, max_length=27, help_text='订单号27位')
    PayJe = serializers.CharField(required=True, help_text='交易金额')
    payType = serializers.CharField(required=True, help_text='1为支付宝，2为微信')
    PayMore = serializers.CharField(required=True, help_text='二维码备注 exp：327-100-03')
