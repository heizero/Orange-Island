import json
import random
import re
import uuid

import requests
from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from  rest_framework.exceptions import ValidationError

from tools.auth import create_token
from wx_api import models
from tools.phone_message import send_message

from django_redis import get_redis_connection


appid ='wx73c4108362999828'
SecretId = '17dc0b786b9f47aa1f1f32ca4ac308a0'

def phone_validator(value):
    if not re.match(r'^(1[3|4|5|6|7|8|9])\d{9}$',value):
        raise ValidationError("手机格式错误")



class MessageSerializer(serializers.Serializer):

    phone=serializers.CharField(label='手机号',validators=[phone_validator,])




class LoginView(APIView):
    def post(self,request,*args,**kwargs):
       # 获取小程序数据
        phone=request.data['phone']
        code=request.data['code']
        wx_code=request.data['wx_code']


        try:
            # 拿手机对比redis查询数
            conn = get_redis_connection()
            a=conn.get(phone)
            print('a',int(a))

            if  int(code) != int(a):
                return Response({'status':False})
            print('wx_code',wx_code)

            info={
                'appid':'wx73c4108362999828',
                'secret':'17dc0b786b9f47aa1f1f32ca4ac308a0',
                'js_code':wx_code,
                'grant_type' : 'authorization_code'
            }
            result=requests.get(url=' https://api.weixin.qq.com/sns/jscode2session'
                         ,params=info
                         )
            print(123,result.json()['openid'])

            openid=result.json()['openid']
            exists=models.UserInfo.objects.filter(openid=openid).exists()
            if not exists:
                models.UserInfo.objects.create(
                    phone=phone,
                    openid=openid,
                )
            else:
                models.UserInfo.objects.filter(openid=openid).update(phone=phone)




        # 1.将wxｃｏｄｅ发送下面网站换取ｏｐｅｎｉｄ
        #     GET
        #     https: // api.weixin.qq.com / sns / jscode2session?
        #     appid = APPID &\
        #      = SECRET & \
        #     js_code = JSCODE & \
        #     grant_type = authorization_code
        # 2.将数据手机号,openid存入数据库


        except Exception as e:
            print('e:',e)
            return Response({'status':False,'message':'请输入正确手机号'})


        # 传入token
        token=create_token({'phone':phone,'openid':openid})



        return Response({'status':True,code:200,'message':'成功注册','token':token})

class MessageView(APIView):
    def get(self,request,*args,**kwargs):

        #手机格式校验
        ser=MessageSerializer(data=request.query_params)
        if not ser.is_valid():
            print(ser.validated_data)
            return Response({'status':False,'message':'手机格式错误'})

        # 获取手机号
        phone=ser.validated_data.get('phone')
        print('is',phone)
        random_code=random.randint(1000,9999)


        # 把验证码＋手机号保留
        #     搭建redis
        conn = get_redis_connection()
        if conn.keys(phone):
            return Response({'status':'false','message':'号码重复'})
        conn.set(phone,random_code,ex=30*15)
            # 发送短信
        # send_message(phone,str(random_code))

        print(random_code)


        # 获取redis值
        a=conn.get(phone)
        print(a)

        return Response({'status':True,'message':'发送成功'})

class AuthoSerializer(serializers.Serializer):
    phone=serializers.CharField(label='手机号',validators=[phone_validator])
    code=serializers.CharField(label='短信验证码')

    def vaildata_code(self,value):
        if len(value)!=4:
            raise ValidationError('短信格式错误')

        if not value.isdecimal():
            raise ValidationError('短信格式错误')
        phone=self.initial.data.get('phone')
        conn=get_redis_connection()
        code=conn.get(phone)
        if not code:
            raise ValidationError('验证码错误')
        if value !=code.decode('utf-8'):
            raise ValidationError('验证码错误')

        return value
#
class AuthorView(APIView):
    def post(self,request,*args,**kwargs):
        '''
        校验手机号
        校验验证码
            没验证码
            验证输入错误
            验证码成功
        去数据库获取用户信息（获取｜验证）
        将一些信息返回给小程序
        '''
        ser=AuthoSerializer(data=request.data)

        # 校验
        if not ser.is_valid():
            return Response({'status':False,'message':'验证码错误'})
        phone=ser.validated_data.get('phone')
        # user=models.UserInfo.objects.filter(phone=phone).first()
        # if not user:
        #     models.UserInfo.objects.create(phone=phone,token=str(uuid.uuid4()))
        # else:
        #     user.token=str(uuid.uuid4())
        #     user.save()


        user_object,flag=models.UserInfo.objects.get_or_create(phone=phone)
        user_object.token=str(uuid.uuid4())
        user_object.save()

        return Response({'status':True,'data':{'token':user_object.token,'phone':phone}})