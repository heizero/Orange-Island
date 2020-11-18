



from django.urls import path,re_path


from wx_api.Views.category import CategoryView
from wx_api.Views.detail import DetailView
from wx_api.Views.index import WaterListView, SwiperListView, RecommendView
from wx_api.Views.search import SearchView





urlpatterns = [

    path('waterlist/',WaterListView.as_view()),
    path('swiperlist/',SwiperListView.as_view()),
    path('recommendlist/',RecommendView.as_view()),
    path('categorylist/',CategoryView.as_view()),
    path('searchlist/',SearchView.as_view()),


    # re_path(r'searchlist//'),


    re_path(r'detaillist/(?P<pk>\d+)/$',DetailView.as_view()),

]