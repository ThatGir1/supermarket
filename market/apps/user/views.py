import hashlib

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from user.forms import RegisterModelForm
from user.models import MarkUser


class RegisterView(View):
    def get(self,request):
        return render(request,'user/reg.html')

    def post(self,request):
        #接收参数
        data=request.POST
        # print(data) 断点：得到 html 中name名为tel password repassword数据
        #实例化表单对象
        #把数据传入验证表单
        register_form=RegisterModelForm(data)
        #验证合法性
        if register_form.is_valid():
            #合法
            #获取清洁后的数据
            cleaned_data=register_form.cleaned_data
            # 操作数据库
            #创建一个用户
            user=MarkUser()
            user.tel=cleaned_data.get('tel')
            #对清洁后的密码加密设置编码
            h=hashlib.md5(cleaned_data.get('password').encode('utf-8'))
            user.password=h.hexdigest()
            return redirect('user:登录')
            # return HttpResponse("合法")

        # 合成响应
        else:
            # return HttpResponse("不合法")
            return render(request,'user/reg.html',{'form':register_form})


class LoginView(View):
    def get(self,request):
        return  render(request,'user/login.html')

    def post(self):
        pass




