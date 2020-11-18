from django.forms import model_to_dict
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from tools.auth import JwtQuerParamsAuthrntication
from wx_api import models
pic=['pic_one','pic_two','pic_three','pic_four','pic_five','pic_six','pic_seven','pic_eight','pic_nine']


class FeedbackModelSerializer(serializers.ModelSerializer):

    class Meta:
        model=models.Feedback
        fields=['description','pic_one','pic_two',
                'pic_three','pic_four','pic_five',
                'pic_six','pic_seven','pic_eight',
                'pic_nine','user_info']





class FeedbackView(APIView):
    authentication_classes = [JwtQuerParamsAuthrntication]
    def post(self,request):
        res=request.data
        data=dict(zip(pic,res['image']))
        data['description']=res['describe']
        # 查找手机号
        user_info=models.UserInfo.objects.filter(phone=res['phone']).first()
        print(type(user_info))
        if not user_info:
            return Response({'status':404,'msg':'请先登录'})


        data['user_info']=user_info.id
        ser=FeedbackModelSerializer(data=data)
        if ser.is_valid():
            ser.save()
            print(ser.data)
            return Response({'status':200,'msg':'ok'})
        return Response({'status':404,'msg':'验证失败'})

"""
{'image': ['heizero-1303825026.cos.ap-nanjing.myqcloud.com/%E9%BB%91zero%2B5q4svo4o16051869710621605186971063.jpg',
            'heizero-1303825026.cos.ap-nanjing.myqcloud.com/%E9%BB%91zero%2B5q4svo4o16051869710621605186971093.jpg'], 
'describe': '123',
'phone': '13775293562'}


"""