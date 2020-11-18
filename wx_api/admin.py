from django.contrib import admin

# Register your models here.
from wx_api import models


class GoodsAdmin(admin.ModelAdmin):
    list_display =['name','intro','sell','image_top','image_id','state','price']
    list_editable =['intro','sell','image_top','image_id','state','price']
    search_fields = ['name','intro','image_top','image_id']
    list_filter=['state']
admin.site.register(models.GoodsModel,GoodsAdmin)


class ImageAdmin(admin.ModelAdmin):
    list_display = ['name','pic_one','pic_two','pic_three','pic_four']
    list_editable =['pic_one','pic_two','pic_three','pic_four']
    search_fields = ['name','pic_one','pic_two','pic_three','pic_four']
admin.site.register(models.ImageModel,ImageAdmin)



class BigKindAdmin(admin.ModelAdmin):
    list_display =['name']
admin.site.register(models.BigKindModel,BigKindAdmin)



class HeadlineAdmin(admin.ModelAdmin):
    list_display =['name']
admin.site.register(models.HeadlineModel,HeadlineAdmin)





class SmallKindAdmin(admin.ModelAdmin):
    list_display =['name','log']
    list_editable =['log']
admin.site.register(models.SmallKindModel,SmallKindAdmin)









class RecommendAdmin(admin.ModelAdmin):
    list_display = ['goods_id']
admin.site.register(models.RecommendModel,RecommendAdmin)


class SwiperAdmin(admin.ModelAdmin):
    list_display=['goods_id']
admin.site.register(models.SwiperModel,SwiperAdmin)




class CommunityAdmin(admin.ModelAdmin):
    list_display=['name','address']
admin.site.register(models.Community,CommunityAdmin)


class ApartmentAdmin(admin.ModelAdmin):
    list_display=['name']
admin.site.register(models.Apartment,ApartmentAdmin)

class FloorAdmin(admin.ModelAdmin):
    list_display=['name']
admin.site.register(models.Floor,FloorAdmin)

class ResidentAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(models.Resident,ResidentAdmin)




class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['phone','openid']
admin.site.register(models.UserInfo,UserInfoAdmin)


class SHOUHUOAdmin(admin.ModelAdmin):
    list_display = ['shouhuo_phone','shouhuo_person']
admin.site.register(models.SHOUHUO,SHOUHUOAdmin)



class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['description','user_info','pic_one','pic_two','pic_three','pic_four','pic_five','pic_six','pic_seven','pic_eight','pic_nine']
admin.site.register(models.Feedback,FeedbackAdmin)

class OrderModel(admin.ModelAdmin):
    list_display = ['orderid','goods','user','address_key','num',
                    'total_price','paystatus','shouhuostatus','backpaystatus']

admin.site.register(models.OrderModel,OrderModel)