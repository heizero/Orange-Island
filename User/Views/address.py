

from rest_framework import serializers, status

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import CursorPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from wx_api import models

#******************************************************

class AddressModelSerializer(serializers.ModelSerializer):

    class Meta:
        model=models.Community
        fields=['id','name','address','apartment_key']
        depth = 3

class AddressView(RetrieveAPIView):
    queryset=models.Community.objects
    serializer_class = AddressModelSerializer


class CommunityModelSerializer(serializers.ModelSerializer):

    class Meta:
        model=models.Community
        fields=['id','name']

class CommunityView(ListAPIView):
    queryset = models.Community.objects
    serializer_class =CommunityModelSerializer