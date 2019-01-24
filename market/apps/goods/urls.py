from django.conf.urls import url

from goods.models import Category
from goods.views import IndexView, DetailView, ListView, CategoryView

urlpatterns = [
    url(r'^/$',IndexView.as_view(),name='主页'),
    url(r'^detail/(?P<id>\d+)/$',DetailView.as_view(),name='详情'),
    url(r'^cate/$', CategoryView.as_view(), name='分类列表'),
    url(r'^list/$',ListView.as_view(),name='店家列表'),


]