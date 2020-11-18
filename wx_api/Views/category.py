from django.forms import model_to_dict
from django.http import HttpResponse
from rest_framework import serializers


from rest_framework.generics import ListAPIView
from rest_framework.pagination import CursorPagination
from rest_framework.views import APIView

from wx_api import models


#*****************************************************

class CategoryViewModelSerializer(serializers.ModelSerializer):

    class Meta:
        model=models.BigKindModel
        fields=['id','name','headline_Mang']
        depth=2




class CategoryView(ListAPIView):
    queryset = models.BigKindModel.objects.all()
    serializer_class = CategoryViewModelSerializer

    # {'id': 1, 'name': '一', 'headline_Mang': [ < HeadlineModel: id:1, 名称：A >, < HeadlineModel: id:2, 名称：B >]}