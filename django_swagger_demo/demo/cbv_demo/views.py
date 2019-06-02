from django.shortcuts import render
from cbv_demo.serializers import ContactDataSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Contact
from rest_framework import status, generics


class ContactData(generics.GenericAPIView):
    serializer_class = ContactDataSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, format=None):
        contacts = Contact.objects.all()
        serializer = ContactDataSerializer(contacts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ContactDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 视图
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from cbv_demo.serializers import UserSerializer, GroupSerializer


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    '''
        list:查看
        create:创建
    '''
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    '''查看，编辑组的界面'''
    queryset = Group
    serializer_class = GroupSerializer
