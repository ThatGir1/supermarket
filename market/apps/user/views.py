import hashlib
import random
import uuid

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from db.base_view import VerifyLoginView
from user.forms import RegisterModelForm, LoginModelForm,  ForgetModelForm
from user.helper import send_sms
from user.models import MarkUser
import re
from django_redis import get_redis_connection


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
            user.save()
            return redirect('user:登录')
            # return HttpResponse("合法")

        # 合成响应
        else:
            # return HttpResponse("不合法")
            return render(request,'user/reg.html',{'form':register_form})


class LoginView(View):
    def get(self,request):
        return  render(request,'user/login.html')

    def post(self,request):
        #接收参数
        data=request.POST
        #创建模型对象
        login_form=LoginModelForm(data)
        #验证合法性
        if login_form.is_valid():
            #从表单中得到清洁后用户信息
            user=login_form.cleaned_data.get('user')
            #保存所需信息到seesion中
            request.session['ID'] =user.pk
            request.session['tel']=user.tel
            #关闭浏览器就消失
            request.session.set_expiry(0)

            return redirect('user:个人中心')


            #合法
            # return  HttpResponse("合法")
        else:
            #合成响应
            return render(request,'user/login.html',{'form':login_form})



class MemberView(VerifyLoginView):
    def get(self,request):
        return render(request,'user/member.html')

    def post(self,request):
        pass




class ForgetView(View):
    def get(self,request):
        return render(request,'user/forgetpassword.html')

    def post(self,request):
        #获取数据
        data=request.POST
        forget_form=ForgetModelForm(data)
        if forget_form.is_valid():

            tel=ForgetModelForm.cleaned_data.get('tel')
            password=ForgetModelForm.cleaned_data.get('password')
            h = hashlib.md5(ForgetModelForm.cleaned_data.get('password').encode('utf-8'))

            user=MarkUser()
            user.objects.filter(tel=tel).update(password=h.hexdigest())
            return redirect('user:个人中心')
            #合法
            #操作数据库

            # MarkUser.objects.
            return redirect('user:登录')
        else:
            return render(request,'user/forgetpassword.html',{'form':forget_form})

        # return HttpResponse('ko')



# class ChangePasswordView(View):
#     def get(self,request):
#         return render(request,'user/forgetpassword.html')
#
#     def post(self,request):
#         pass
#         #接收参数
#         data=request.POST
#         Change_form=ChangePasswordModelForm(data)
#
#         #操作数据库
#         #合成响应

class SendMsm(View):
    """发送短信"""
    def get(self,request):
        pass

    def post(self,request):
        #1.接受参数
        tel=request.POST.get('tel','')
        # 匹配不到位none 匹配到是一个对象
        rs=re.search('^1[3-9]\d{9}$',tel)
        if rs is None:
            return JsonResponse({'error':1,'errmsg':'电话号码格式错误'})

        #2.处理数据
        #模拟，后再接入运营商
        """
            1.生成随机的验证码
            2.保存验证码道redis
            3.接入运营商
        """
        #1.生成随机验证码
        #列表推倒式是个列表
        # [str(random.randint(0,9)for _ in range(6))]
        #拼接字符串
        random_code="".join([str(random.randint(0,9)) for _ in range(6)])


        print('**************随机验证码为****{}********************'.format(random_code))

        #2.保存验证码到redis中
        #获取连接
        r=get_redis_connection()
        r.set(tel,random_code)
        #保存手机发送验证码次数不超过5次
        #受限获取当前手机号码发送的次数

        r.expire(tel, 60)  # 设置60秒后过期

        # 首先获取当前手机号码的发送次数
        key_times = "{}_times".format(tel)
        now_times = r.get(key_times)  # 从redis获取的二进制,需要转换
        # print(int(now_times))
        if now_times is None or int(now_times) < 5:
            # 保存手机发送验证码的次数, 不能超过5次
            r.incr(key_times)
            # 设置一个过期时间
            r.expire(key_times, 3600)  # 一个小时后再发送
        else:
            # 返回,告知用户发送次数过多
            return JsonResponse({"error": 1, "errmsg": "发送次数过多"})


        #接入运营商
        __business_id = uuid.uuid1()
        params = "{\"code\":\"%s\",\"product\":\"景一机车服店\"}"% random_code
        print(send_sms(__business_id,tel, "注册验证", "SMS_2245271", params))
        print(rs.decode('utf-8'))


        #3.合成响应
        return JsonResponse({'error':0})


