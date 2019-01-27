from django.conf.urls import url

from goods.models import Category
from goods.views import DetailView, ListView, CategoryView,IndexView

urlpatterns = [
    url(r'^detail/(?P<id>\d+)/$',DetailView.as_view(),name='详情'),
    url(r'^cate/(?P<cate_id>\d*)_{1}(?P<order>\d?)\.html$', CategoryView.as_view(), name='分类列表'),
    url(r'^list/$',ListView.as_view(),name='店家列表'),
    url(r'^$',IndexView.as_view(),name='主页'),



]