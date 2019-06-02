from rest_framework import serializers
from .models import Contact


class ContactDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


# 序列化
from django.contrib.auth.models import User, Group


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"
