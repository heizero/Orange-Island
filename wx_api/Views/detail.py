from django.forms import model_to_dict
from rest_framework import serializers
from rest_framework.generics import RetrieveAPIView
from rest_framework.serializers import Serializer

from wx_api import models


class DetailModelSerializer(serializers.ModelSerializer):
    image_id=serializers.SerializerMethodField()
    class Meta:
        model=models.GoodsModel
        # fields=['name','image_id']
        fields=['id','name','intro','price','image_top','state','unit','image_id','update_time']
    def get_image_id(self,obj):
        print('id',obj.image_id)
        if not obj.image_id:
            return
        image_id=models.ImageModel.objects.filter(id=obj.image_id.id).values(
            'id',
            'pic_one',
            'pic_two',
            'pic_three',
            'pic_four'
        )

        return image_id[0]




class DetailView(RetrieveAPIView):
    queryset = models.GoodsModel.objects
    serializer_class = DetailModelSerializer