from django.conf.urls import url

from user.views import index, register, login

urlpatterns = [
    url(r'^$',index,name='主页'),
    url(r'^register/$',register,name='注册'),
    url(r'^login/$',login,name='登录'),
]