from django.conf.urls import url

from goods.views import IndexView, DetailView, ListView

urlpatterns = [
    url(r'^index/$',IndexView.as_view(),name='主页'),
    url(r'^detail/$',DetailView.as_view(),name='详情'),
    url(r'^list/$',ListView.as_view(),name='列表'),

]