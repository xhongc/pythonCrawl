from rest_framework import serializers


class QmforderSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=False, help_text='查询页数')
    trade_type = serializers.CharField(required=False, help_text='支付类型 Alipay 2.0为支付宝 WXPay为微信支付')
    switch = serializers.CharField(required=False, help_text='备注开关 1为开')
