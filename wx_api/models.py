from django.db  import models

from db.base_model import BaseModel



class ImageModel(BaseModel):
    name=models.CharField(verbose_name='名称',max_length=30)
    pic_one=models.CharField(verbose_name='图片1',max_length=255)
    pic_two=models.CharField(verbose_name='图片2',max_length=255)
    pic_three=models.CharField(verbose_name='图片3',max_length=255)
    pic_four=models.CharField(verbose_name='图片4',max_length=255)

    def __str__(self):
        return 'id:%d,名称:%s'%(self.id,self.name)


    class Meta:
        verbose_name = '图片表'
        verbose_name_plural = '图片表'

    # 小种类表
class SmallKindModel(BaseModel):
    name = models.CharField(verbose_name='小种类', max_length=30)
    log = models.CharField(verbose_name='图片', max_length=300)

    def __str__(self):
        return 'id:%d,名称：%s,log:%s' % (self.id, self.name, self.log)

    class Meta:
        verbose_name = '小种类表'
        verbose_name_plural = '小种类表'

# 标题模型
class HeadlineModel(BaseModel):
    name = models.CharField(verbose_name='标题', max_length=30)
    smallkind_Mang = models.ManyToManyField(verbose_name='标题表（大多）',
                                                to=SmallKindModel,
                                                related_name='smallkind_Mang', )

    def __str__(self):
        return 'id:%d,名称：%s' % (self.id, self.name)

    class Meta:
        verbose_name = '标题表'
        verbose_name_plural = '标题表'
# 大众类模型
class BigKindModel(BaseModel):
    name=models.CharField(verbose_name='大种类',max_length=30)
    headline_Mang=models.ManyToManyField(verbose_name='标题表（大多）',
                                         to=HeadlineModel,
                                         related_name='headline_Mang',)


    def __str__(self):
        return 'id:%d,名称：%s' %(self.id,self.name)
    class Meta:
        verbose_name = '大种类表'
        verbose_name_plural = '大种类表'



# 商品模型
class GoodsModel(BaseModel):
    name=models.CharField(verbose_name='名称',max_length=30)
    intro=models.CharField(verbose_name='简介',max_length=300)
    sell=models.PositiveIntegerField(verbose_name='销量')
    image_top=models.CharField(verbose_name='图片',max_length=255)
    brank = models.CharField(verbose_name='品牌', max_length=50)
    unit = models.CharField(verbose_name='单位', max_length=80)
    price = models.PositiveIntegerField(verbose_name='价格')
    # 图片外键
    image_id=models.ForeignKey(verbose_name='图片(外）',to='ImageModel',
                               on_delete=models.SET_NULL,blank=True,
                               related_name='image_id',null=True)
    state=models.BooleanField(verbose_name='状态',default=True)

    kind=models.ManyToManyField(verbose_name='种类',to=SmallKindModel,
                                related_name='Gsmall_many')

    is_delete = models.BooleanField(default=False, verbose_name='删除标记')
    def __str__(self):
        return 'id:%d,名称,%s,销量%d,是否在售%d,种类%s'%(self.id,self.name,self.sell,self.state,self.kind)

    class Meta:
        verbose_name = '商品表'
        verbose_name_plural = '商品表'




# 首页推荐模型
class RecommendModel(BaseModel):
    goods_id=models.ForeignKey(verbose_name='商品(外）', to='GoodsModel',
                                 on_delete=models.SET_NULL, blank=True,
                               related_name='Rgoods_id',null=True,)
    def __str__(self):
        return  '商品id_id%d'%(self.goods_id_id)

    class Meta:
        verbose_name = '推荐表'
        verbose_name_plural = '推荐表'
# 首页轮播图
class SwiperModel(BaseModel):
    goods_id = models.ForeignKey(verbose_name='商品(外）', to='GoodsModel',
                                 on_delete=models.SET_NULL, blank=True,
                                 related_name='Sgoods_id',null=True,)
    def __str__(self):
        return  '商品id_id%d'%(self.goods_id_id)

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = '轮播图'






# 地址表


class Resident(models.Model):
    name=models.CharField(verbose_name='住户地址',max_length=20)

    def __str__(self):
        return '住户%s' % (self.name)

    class Meta:
        verbose_name = '住户'
        verbose_name_plural = verbose_name

class Floor(models.Model):
    name=models.CharField(verbose_name='楼层名称',max_length=20)
    resident_key=models.ManyToManyField(verbose_name='住户',to=Resident)



    def __str__(self):
        return  '楼层%s 住户%s'%(self.name,self.resident_key)

    class Meta:
        verbose_name = '楼层名称'
        verbose_name_plural = verbose_name


class Apartment(models.Model):
    name=models.CharField(verbose_name='单元楼',max_length=30)
    floor_key=models.ManyToManyField(verbose_name='楼层',to=Floor)

    def __str__(self):
        return  '单元楼%s 地址%s'%(self.name,self.floor_key)

    class Meta:
        verbose_name = '单元楼'
        verbose_name_plural = verbose_name



class Community(models.Model):
    name=models.CharField(verbose_name='小区名',max_length=50)
    address=models.CharField(verbose_name='地址',max_length=100)
    apartment_key=models.ManyToManyField(verbose_name='单元楼',to=Apartment)

    def __str__(self):
        return  '小区名%s 地址%s,楼层表%s'%(self.name,self.address,self.apartment_key)

    class Meta:
        verbose_name = '小区'
        verbose_name_plural = verbose_name




# 可以创个总地址表然后把各个小区的地址一对多写进去
# class address(models.Model):
#
#     name=models.CharField(verbose_name='名称',null=True,blank=True,max_length=200,default='暂无')
#
#     community_key=models.ForeignKey(verbose_name='小区',to=Community,
#                                     on_delete=models.SET_NULL,blank=True,null=True)
#



class UserInfo(BaseModel):

    phone=models.CharField(verbose_name='手机号',max_length=11)

    openid=models.CharField(verbose_name='openid',max_length=100)

    def __str__(self):
        return '手机号%s openid%s' % (self.phone, self.openid)

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = verbose_name


class SHOUHUO(BaseModel):


    shouhuo_phone=models.CharField(verbose_name='收货手机号',max_length=11)

    shouhuo_person=models.CharField(verbose_name='收货人',max_length=20,)

    address_key = models.ManyToManyField(verbose_name='地址表', to=Community)
    is_delete = models.BooleanField(default=False, verbose_name='删除标记')

    def __str__(self):
        return '收货手机号%s 收货人%s　收货地址%s 是否删除%s' % (self.shouhuo_phone,
                                         self.shouhuo_person,
                                         self.address_key,
                                         self.is_delete
                                            )

    class Meta:
        verbose_name = '收货表'
        verbose_name_plural = verbose_name



class OrderModel(BaseModel):

    """ 订单表 """

    orderid = models.CharField(verbose_name='订单号',max_length=64)

    goods = models.ForeignKey(verbose_name='商品',to='GoodsModel',on_delete=models.SET_NULL,blank=True,null=True)
    user =  models.ForeignKey(verbose_name='用户',to='UserInfo',on_delete=models.SET_NULL,blank=True,null=True)
    address_key=models.ForeignKey(verbose_name='收货表',to='SHOUHUO',on_delete=models.SET_NULL,blank=True,null=True)
    num=models.SmallIntegerField(verbose_name='数量')
    total_price=models.SmallIntegerField(verbose_name='单个总价')
    paystatus = models.BooleanField(verbose_name='支付状态',default=False)
    shouhuostatus = models.BooleanField(verbose_name='收货状态', default=False)
    # 退货标签
    backpaystatus=models.BooleanField(verbose_name='退货',default=False)

    def __str__(self):
        return '订单号%s 商品%s　用户%s 收货%s　数量%s 单个总价%s ' \
               '支付状态%s 收货状态%s 创建时间%s 更新时间%s 退货%s' % ( self.orderid,
                                                                    self.goods,self.user,self.address_key,self.num,
                                                                    self.total_price,self.paystatus,
                                                      self.shouhuostatus,self.create_time,self.update_time,self.backpaystatus)
    class Meta:
        verbose_name = '订单表'
        verbose_name_plural = verbose_name


class Feedback(BaseModel):


    description=models.CharField(verbose_name='描述',max_length=300)
    pic_one=models.CharField(verbose_name='图片１',max_length=300)
    pic_two=models.CharField(verbose_name='图片２',max_length=300,blank=True,null=True)
    pic_three=models.CharField(verbose_name='图片３',max_length=300,blank=True,null=True)
    pic_four=models.CharField(verbose_name='图片４',max_length=300,blank=True,null=True)
    pic_five=models.CharField(verbose_name='图片５',max_length=300,blank=True,null=True)
    pic_six=models.CharField(verbose_name='图片６',max_length=300,blank=True,null=True)
    pic_seven=models.CharField(verbose_name='图片７',max_length=300,blank=True,null=True)
    pic_eight=models.CharField(verbose_name='图片８',max_length=300,blank=True,null=True)
    pic_nine=models.CharField(verbose_name='图片９',max_length=300,blank=True,null=True)
    user_info=models.ForeignKey(verbose_name='用户',to='UserInfo',on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return '描述%s 图片１%s　图片２%s 图片３%s 图片４%s ' \
               '图片５%s 图片６%s　图片７%s　图片８%s　图片９%s 用户%s' %(
            self.description,self.pic_one,self.pic_two,self.pic_three,self.pic_four,self.pic_five,self.pic_six,self.pic_seven,
            self.pic_eight,self.pic_nine,self.user_info)

    class Meta:
        verbose_name = '意见表'
        verbose_name_plural = verbose_name































