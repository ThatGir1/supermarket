from django.conf.urls import url

from user.views import RegisterView, LoginView, MemberView

urlpatterns = [
    url(r'^register/$',RegisterView.as_view(),name='注册'),
    url(r'^login/$',LoginView.as_view(),name='登录'),
    url(r'^member/$', MemberView.as_view(), name='个人中心')
]