from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from user.forms import RegisterModelForm
from user.helper import set_password
from user.models import SpUsers


class RegisterView(View):
    def get(self,request):
        return render(request,'user/reg.html')

    def post(self,request):
        #接收参数
        data=request.POST
        #实例化form表单对象
        form=RegisterModelForm(data)
        #验证数据合法性
        if form.is_valid():
            #合法
            #获取清洁后数据
            cleaned_data=form.cleaned_data
            #创建一个用户
            user = SpUsers()
            user.tel=cleaned_data.get('tel')
            user.password=set_password(cleaned_data.get('repassword'))
            user.save()
            return redirect('user:登录')
        else:
            return render(request,'user/reg.html',{'form':form})






class LoginView(View):
    def get(self,request):
        return render(request,'user/login.html')

    def post(self,request):
        pass
