from django.conf.urls import url

from user.views import RegisterView, LoginView, MemberView, ForgetView, SendMsm,InfoView

urlpatterns = [
    url(r'^register/', RegisterView.as_view(),name='注册'),
    url(r'^login/',LoginView.as_view(),name='登录'),
    url(r'^member/', MemberView.as_view(),name='个人中心'),
    # url(r'^changepwd/', ChangePasswordView.as_view(),name='修改密码'),
    url(r'^forget/', ForgetView.as_view(),name='忘记密码'),
    url(r'^sendMsg/',SendMsm.as_view(),name='发送短信验证码'),
    url(r'^info/',InfoView.as_view(),name='个人资料'),
]
