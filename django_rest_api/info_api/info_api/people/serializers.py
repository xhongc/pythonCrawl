from rest_framework import serializers
from .models import People


class PeopleSeriazars(serializers.ModelSerializer):
    username = serializers.CharField(required=True,label='用户名',
                                     error_messages={'required':'请输入用户名'})
    money = serializers.DecimalField(required=True,label='金额',max_digits=9, decimal_places=2,
                                     error_messages={'required':'请输入金额',
                                                     'decimal_places':'最大保留两位小数'})
    class Meta:
        model = People
        fields = "__all__"
