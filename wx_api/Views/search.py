
from rest_framework import serializers, status


from rest_framework.pagination import CursorPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from wx_api import models
#*********************************************************************************
class IdResultsSetPagination(CursorPagination):
    # URL传入的游标参数
    cursor_query_param = 'cursor'
    # 默认每页显示的数据条数
    page_size = 5
    # URL传入的每页显示条数的参数
    page_size_query_param = 'page_size'
    # 每页显示数据最大条数
    max_page_size = 12

    # 根据ID从大到小排列
    ordering = "-id"

class SellResultsSetPagination(CursorPagination):
    # URL传入的游标参数
    cursor_query_param = 'cursor'
    # 默认每页显示的数据条数
    page_size = 5
    # URL传入的每页显示条数的参数
    page_size_query_param = 'page_size'
    # 每页显示数据最大条数
    max_page_size = 12

    # 根据ID从大到小排列
    ordering = "-sell"

class PriceResultsSetPagination(CursorPagination):
    # URL传入的游标参数
    cursor_query_param = 'cursor'
    # 默认每页显示的数据条数
    page_size = 5
    # URL传入的每页显示条数的参数
    page_size_query_param = 'page_size'
    # 每页显示数据最大条数
    max_page_size = 12

    # 根据ID从小到大排列
    ordering = "price"

class SearchModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.GoodsModel
        fields=['id','name','intro','sell','image_top','brank','price','unit','state']

class SearchView(APIView):
    def get(self,request):
        # res = request.query_params
        # res=json.loads(res['data'])
        # print(res)
        # Kind_obj=models.SmallKindModel.objects.filter(Q(id=res['id'])|
        #                                         Q(name=res['name'])).first()
        #
        #
        # print(Kind_obj)
        # good_list=Kind_obj.Gsmall_many.all()
        # print(good_list)
        #
        # return HttpResponse('123')

        res = request.query_params.dict()
        token1 = request.META.get('HTTP_REMOTE_ADDR')
        print('TOKEN', token1)

        if not res:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if 'id' in res:
            Kind_obj = models.GoodsModel.objects.filter(kind__smallkind_Mang__id=res['id']).distinct()

        elif 'name' in res:
            Kind_obj = models.GoodsModel.objects.filter(name__icontains=res['name']).order_by('-id').distinct()
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not 'params' in res:
            pg = IdResultsSetPagination()
            pages = pg.paginate_queryset(queryset=Kind_obj, request=request)
            ser = SearchModelSerializer(instance=pages, many=True)
            return pg.get_paginated_response(ser.data)

        if res['params']=="1":
            pg = SellResultsSetPagination()
        elif res['params']=='2':
            pg=PriceResultsSetPagination()


        pages = pg.paginate_queryset(queryset=Kind_obj, request=request)
        ser = SearchModelSerializer(instance=pages, many=True)
        return pg.get_paginated_response(ser.data)






































