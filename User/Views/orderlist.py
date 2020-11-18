import datetime
import random

import requests
import time

from django.db.models import Q
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from xml.etree import ElementTree as ET
import hashlib

from tools.auth import JwtQuerParamsAuthrntication
from wx_api import models


import json
import os

from sts.sts import Sts


def md5(string):
    m=hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()



appid ='wx73c4108362999828'
SecretId = '17dc0b786b9f47aa1f1f32ca4ac308a0'
# 商户号
# 商户秘钥
pay_key='1213'#商户秘钥
class PaymentView(APIView):


    def post(self,request,*args,**kwargs):
        res = request.data
        price = res['order_price']
        phone = res['phone']
        goods_list = [i for i in res['goods']]
        shouhuo_info = res['consiginee_add']

        # 商品列表查询价格和数量和价格做对比
        print(goods_list, type(goods_list))
        total_price=0
        for i in goods_list:
            goodsprice = models.GoodsModel.objects.filter(id=i['id']).values('price')
            print(goodsprice[0]['price'], '1qweqw23', i['price'])
            if i['price'] != goodsprice[0]['price']:
                return Response({'status': 201, 'msg': '数据不匹配'})
            # 数量*价格＝总价
            total_price =total_price+ i['num'] * i['price']


        info = {
            'appid': appid, #小程序号　　小程序申请
            'mch_id': '１',  #商户号　　小程序申请
            'device_info': '#设备信息',   #设备信息
            'nonce_str': "",#随机字符串
            'sign_type': "MD5",#加密类型
            'body': "商品的描述信息",  #商品的描述信息
            'detail': '这是一个商品详细描述信息.',#这是一个商品详细描述信息. 可以不填
            'attach': '附加数据，ｘｘ小程序',#这是一个商品附加数据. 可以不填
            'out_trade_no': '1',#订单号 要求32个字符内，只能是数字、大小写字母_-|*且在同一个商户号下唯一
            'total_fee': '123',  # 总金额 单位分
            'spbill_create_ip': request.META.get('REMOTE_ADDR'),  # 终端IP（用户IP） remote_addr = request.META.get('REMOTE_ADDR')
            'notify_url': "成功支付后ｗｘ调用的ａｐｉ",  # 支付成功之后，微信异步通知
            'trade_type': 'JSAPI',
            'openid': 123  # openid　通过ｃｏｄｅ获取的openid
        }

        # 签名
            #排序 sorted
            #拼接
            #加上商户秘钥

        temp='&'.join(['{0}={1}'.format(k,info[k])for k in sorted(info)]+["{0}={1}".format('key',pay_key,)])
            #md5加密
        sign=md5(temp).upper()
            #将加密sign加入ｉｎｆｏ
        info['sign']=sign
            #将dict转成xml字符串
        xml_string="<xml>{0}</xml>".format("".join(["<{0}>{1}</{0}>".format(k,v)for k,v in info.items()]))
            #发送数据
        prepay=requests.post('https://api.mch.weixin.qq.com/pay/unifiedorder',data=xml_string.encode('utf-8'))
        print(prepay.text)
        #★★★★拿到prepay_id

        root=ET.XML(prepay.content.decode('utf-8'))
        prepay_dict={child.tag:child.text for child in root}
        prepay_id=prepay_dict['prepay_id']
        print(prepay_id)

        #再次签名+++++++++++++++++++++++++++++++

        info_dict={
            'appid': appid, #小程序号　　小程序申请
            'timeStamp':str(int(time.time())),
            'nonce_str': "".join([chr(random.randint(65, 90)) for _ in range(12)]),#随机字符串
            'package':'prepay_id={0}'.format(prepay_dict),
            'signType':'MD5'
        }
        temp='&'.join(
            ["{0}={1}".format(k,info_dict[k]) for k in sorted(info_dict)]+['{0}={1}'.format('key',pay_key),]
        )
        sign2=md5(temp).upper()
        info_dict['paySign']=sign2

        return Response(info_dict)



class OrderView(APIView):

    def post(self,request,*args,**kwargs):
        res = request.data
        price=res['order_price']
        phone=res['phone']
        goods_list=[i for i in res['goods']]
        shouhuo_info=res['consiginee_add']

        # 商品列表查询价格和数量和价格做对比
        print(goods_list, type(goods_list))

        for i in goods_list:
            goodsprice=models.GoodsModel.objects.filter(id=i['id']).values('price')
            print(goodsprice[0]['price'],'1qweqw23',i['price'])
            if i['price'] !=goodsprice[0]['price']:
                return Response({'status':201,'msg':'数据不匹配'})
            # 数量*价格＝总价
            total_price=i['num']*i['price']
            # 保存到数据库


        #在订单表里绑定用户
        print(phone)
        #在定表里绑定收货地址，收货人，电话
        print(shouhuo_info)
        return Response({'status':200,'msg':'ojbk'})



# wx支付完成调用该ａｐｉ
class NotifyView(APIView):

    # 在这个类里改变paystatus状态)
    def post(self,request):
        # 1,wx发送ｘｍｌ的数据request.body
        root = ET.XML(request.body.decode('utf-8'))
        # 2,将xml转成字典
        result={child.tag:child.text for child in root}
        # 获取ｗｘ给的ｓｉｇｎ
        sign=result.pop('sign')
        #3,order_id订单号{商户号，ｏｐｅｎｉｄ,out_trade_no,sign}

        key='商户秘钥'
        temp="&".join(["{0}={1}".format(k,result[k])for k in sorted(result)]
                      +["{0}={1}".format("key",key),])
        # 自己加密的订单
        local_sign=md5(temp).upper()
        #4,校验
        if local_sign==sign:
            #获取订单号
            out_trade_no=result.get('out_trade_no')
        #5,将订单状态更新
            # 按订单号查询数据将状态改成已支付
            models.OrderModel.objects.filter(orderid=out_trade_no).update(paystatus=True)
        #6,返回特定数据（确定自己已经收到更新信息）
            response = """<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>"""
            return Response(response)


# 意见反馈临时秘钥
class get_credential(APIView):
    def get(self,request):

        config = {
            'url': 'https://sts.tencentcloudapi.com/',
            'domain': 'sts.tencentcloudapi.com',
            # 临时密钥有效时长，单位是秒
            'duration_seconds': 1800,
            'secret_id': 'AKIDlFTO42L8F56sMZJAYfU8WfcCYnlalrhI',
            # 固定密钥
            'secret_key':'YvBOzJkYse9SgcIgfLkrhTzKPq77rM2S' ,
            # 设置网络代理
            # 'proxy': {
            #     'http': 'xx',
            #     'https': 'xx'
            # },
            # 换成你的 bucket
            'bucket': 'heizero-1303825026',
            # 换成 bucket 所在地区
            'region': 'ap-nanjing',
            # 这里改成允许的路径前缀，可以根据自己网站的用户登录态判断允许上传的具体路径
            # 例子： a.jpg 或者 a/* 或者 * (使用通配符*存在重大安全风险, 请谨慎评估使用)
            'allow_prefix': '*',
            # 密钥的权限列表。简单上传和分片需要以下的权限，其他权限列表请看 https://cloud.tencent.com/document/product/436/31923
            'allow_actions': [

                'name/cos:PostObject',
                'name/cos:DeleteObject',

            ],

        }

        try:
            sts = Sts(config)
            response = sts.get_credential()
            print('get data : ' + json.dumps(dict(response), indent=4))
            return Response(response)
        except Exception as e:
            print(e)



class OrderListSerializers(serializers.ModelSerializer):
    class Meta:
        model=models.OrderModel
        fields="__all__"

# 订单
class OrderList(APIView):
    authentication_classes = [JwtQuerParamsAuthrntication]
    def post(self,request):
        res = request.data
        print(type(res),res['phone'])
        quarset=models.OrderModel.objects.filter(Q(user__phone=res['phone'])&Q(update_time__contains=datetime.datetime.now()))
        ser=OrderListSerializers(instance=quarset,many=True)

        return Response(ser.data)


# 退货
# 订单


class BlackpayView(APIView):
    authentication_classes = [JwtQuerParamsAuthrntication]
    def post(self,request):
        token1 = request.META.get("HTTP_AUTHORIZATION")
        print(token1)
        res = request.data
        models.OrderModel.objects.filter(id=res['id']).update(backpaystatus=True)

        return Response({'status':200,'msg':'您的订单我们已接收'})

