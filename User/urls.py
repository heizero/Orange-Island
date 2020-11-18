
from django.urls import path,re_path

from User.Views.address import AddressView, CommunityView
from User.Views.feedback import FeedbackView
from User.Views.orderlist import OrderView, get_credential, OrderList, BlackpayView
from User.Views.phone import MessageView, LoginView

urlpatterns = [

    path('communitylist/',CommunityView.as_view()),
    re_path(r'addresslist/(?P<pk>\d+)/$',AddressView.as_view()),
    path('message/',MessageView.as_view()),
    path('login/',LoginView.as_view()),
    path('orderlist/', OrderView.as_view()),
    path('get_credential/', get_credential.as_view()),
    path('get_feedbackView/', FeedbackView.as_view()),
    path('order/', OrderList.as_view()),
    path('black/', BlackpayView.as_view()),


]