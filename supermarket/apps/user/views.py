from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View

from db.base_view import VerifyLoginView
from user.forms import RegisterModelForm, LoginModelForm
from user.helper import set_password, login,check_login
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
        #获取数据
        data=request.POST
        #验证合法性
        #操作数据库
        login_form=LoginModelForm(data)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            login(request, user)
            #合成响应
            # return redirect('user:个人中心')
            return HttpResponse("ko")

        else:
            return render(request, 'user/login.html', {'form': login_form})


class MemberView(VerifyLoginView):
    """个人中心"""
    # @method_decorator(check_login)
    def get(self,request):
        return render(request,'user/member.html')

    # @method_decorator(check_login)
    def post(self,request):
        pass
