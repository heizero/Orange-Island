from django.forms import model_to_dict
from django.http import HttpResponse
from rest_framework import serializers


from rest_framework.generics import ListAPIView
from rest_framework.pagination import CursorPagination

from wx_api import models
# **************************************************************************************

class GoodsModelSerializer(serializers.ModelSerializer):
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)
    class Meta:
        model=models.GoodsModel
        fields=['id','name','intro','sell','image_top','state','update_time','price','unit']

class StandardResultsSetPagination(CursorPagination):
    # URL传入的游标参数
    cursor_query_param = 'cursor'
    # 默认每页显示的数据条数
    page_size = 10
    # URL传入的每页显示条数的参数
    page_size_query_param = 'page_size'
    # 每页显示数据最大条数
    max_page_size = 1000

    # 根据ID从大到小排列
    ordering = "id"

class WaterListView(ListAPIView):
    '''
    １序列化
    ２拿数据（倒叙）
    ３分页
    '''
    serializer_class =GoodsModelSerializer
    queryset = models.GoodsModel.objects.all().order_by('-id')
    pagination_class = StandardResultsSetPagination



#*********************************************************************************************************


class SwiperModelSerialzer(serializers.ModelSerializer):
    goods_id=serializers.SerializerMethodField()
    class Meta:
        model = models.SwiperModel
        fields =['id','goods_id']
    def get_goods_id(self,obj):
        return model_to_dict(obj.goods_id,
                             fields=['id','image_top'])



class SwiperListView(ListAPIView):
    # １、序列化
    serializer_class = SwiperModelSerialzer
    # ２．拿数据
    queryset = models.SwiperModel.objects.all().order_by('-id')[:5]



#*******************************************************************************************************************



class RecommendModelSerialzer(serializers.ModelSerializer):
    goods_id=serializers.SerializerMethodField()
    class Meta:
        model = models.SwiperModel
        fields =['id','goods_id']
    def get_goods_id(self,obj):
        return model_to_dict(obj.goods_id,
                             fields=['id','name','intro','sell','image_top','state','update_time','price','unit'])

class RecommendView(ListAPIView):
    serializer_class = RecommendModelSerialzer
    queryset = models.RecommendModel.objects.all().order_by('-id')[:4]



def image_url(request):
    a='https://heizero-1303825026.cos.ap-nanjing.myqcloud.com/1%20'
    for i in range(50):
        models.ImageModel.objects.create(name=str(i+1),pic_one=a+'('+str((i+121))+').jpg',
                                         pic_two=a + '(' + str((i+122))+ ').jpg',
                                         pic_three=a + '(' + str((i+123)) + ').jpg',
                                         pic_four=a + '(' + str((i+124)) + ').jpg' )
    return HttpResponse('成功')
def goods(request):
    b = 'https://heizero-1303825026.cos.ap-nanjing.myqcloud.com/1%20'
    a='“自己”是看不见的，跟什么东西相撞反弹回来才会了解自己,所以跟强大的、可怕的、水准高的东西相撞，然后才会知道自己是什么'


    for i in range(50):
        image=models.ImageModel.objects.filter(id=i+1).first()

        models.GoodsModel.objects.create(name=str(i),intro=str(i)+a,sell=100+i,
                                         image_top=b+'('+str((i+121))+').jpg',brank='无',
                                         unit='500g',price=i+12,image_id=image,state=True,
                                         )

    return HttpResponse('成功')




def bigkind(request):

    a=['热门推荐','水果蔬菜',
   '配套食材',
   '火锅烧烤',
   '零食饮料',
   '酒水乳饮',
   '粮油副食',
   '废品回收',
   '洗漱用品',
   '儿童玩具',
   '家庭用具',
   '工作学习',]

    for i in a:
        models.BigKindModel.objects.create(name=i)

    return HttpResponse('成功')
#
def addd(request):
   pass



def log (request):

    a=['热门推荐','水果蔬菜',
   '配套食材',
   '火锅烧烤',
   '零食饮料',
   '酒水乳饮',
   '粮油副食',
   '废品回收',
   '洗漱用品',
   '儿童玩具',
   '家庭用具',
   '工作学习',]
    log='https://heizero-1303825026.cos.ap-nanjing.myqcloud.com/1%20(172).jpg'
    for i in a:
        models.SmallKindModel.objects.create(name=i,log=log)


    return HttpResponse


