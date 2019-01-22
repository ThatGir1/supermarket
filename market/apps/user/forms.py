import hashlib

from django import forms
from django.core.validators import RegexValidator
from django_redis import get_redis_connection

from user.models import MarkUser


class RegisterModelForm(forms.ModelForm):
    password = forms.CharField(max_length=16,
                               min_length=6,
                               # error_messages获取表单字段错误信息
                               error_messages={
                                   'required': '密码不能为空',
                                   'max_length': '最大长度为16位',
                                   'min_length': '最小长度为6位',
                               })  # CharField用于接收文本
    repassword = forms.CharField(error_messages={
        'required': '请确认密码',
    })
    captcha=forms.CharField(max_length=6,
                            error_messages={
                                'required':'验证码必须填写'
                            })

    agree =forms.BooleanField(error_messages={
                                'required':'必须同意用户协议'
    })

    class Meta:
        # 关联模型
        model = MarkUser
        # 验证需要的字段
        fields = ['tel', ]
        error_messages = {'tel':
                              {'required': '手机号码不能为空'}
                          }

    def clean_tel(self):
        # 验证手机号码是否重复
        # 获取清洁后的数据tel
        tel = self.cleaned_data.get('tel')
        # 去数据库查询数据是否存在
        repeat_judge = MarkUser.objects.filter(tel=tel).exists()
        if repeat_judge:
            # 抛出一个错误信息
            raise forms.ValidationError('手机号码已经注册')
        else:
            return tel



    def clean(self):
        # 验证密码是否重复
        # 1.获取两次的密码数据
        pwd = self.cleaned_data.get('password')
        pwd1 = self.cleaned_data.get('repassword')
        if pwd and pwd1 and pwd != pwd1:
            raise forms.ValidationError('两次密码不一致')


        #综合校验
        # 验证用户传入验证码跟redis中的是否一样
        try:
            captcha = self.cleaned_data.get('captcha')
            tel = self.cleaned_data.get('tel', '')
            # 获取redis中的
            r = get_redis_connection()
            random_code = r.get(tel)  # 二进制, 转码
            random_code = random_code.decode('utf-8')
            # 比对
            if captcha and captcha != random_code:
                raise forms.ValidationError({"captcha": "验证码输入错误!"})
        except:
            raise forms.ValidationError({"captcha": "验证码输入错误!"})

        # 返回清洁后的数据
        return self.cleaned_data





class LoginModelForm(forms.ModelForm):
    class Meta:
        # 关联模型
        model = MarkUser
        # 需要验证的字段
        fields = ['tel', 'password']
        # 验证字段是否为空
        error_messages = {
            'tel': {
                'required': '请填写手机号'
            },
            'password': {
                'required': '请填写密码'
            }
        }

    def clean(self):
        # 获取用户名和密码
        tel = self.cleaned_data.get('tel')
        password = self.cleaned_data.get('password')
        # 根据获取数据查询数据库
        # get获取数据库如果没有会报错，所以加try
        # 查询数据库中tel用户的所有信息
        try:
            user = MarkUser.objects.get(tel=tel)
        except MarkUser.DoesNotExist:
            raise forms.ValidationError({'tel': '手机号码错误'})

        # 验证密码md5正向不可逆所以验证密码必须给获取密码数据进行编码加密
        h = hashlib.md5(self.cleaned_data.get('password').encode('utf-8'))
        if user.password != h.hexdigest():
            raise forms.ValidationError({'password': '密码错误'})

        # 将用户信息保存到cleaned_data中
        self.cleaned_data['user'] = user
        return self.cleaned_data


# class ChangePasswordModelForm(forms.ModelForm):
#     password = forms.CharField(error_messages={
#                                     'required':'请输入密码'
#     })
#     class Meta:
#         #关联模型
#         model = MarkUser
#         #需要验证的字段
#         fields=['password',]
#         # 验证字段是否为空
#         error_messages = {
#             'password': {
#                 'required': '请填写密码'
#             }
#         }
#
#     def clean_tel(self):
#         #验证手机号码是否存在
#         #获取清洁后的数据tel
#         tel=self.cleaned_data.get('tel')
#         #去数据库查询数据是否存在
#         exists_judge=MarkUser.objects.filter(tel=tel).exists()
#         if exists_judge:
#             #返回一个tel
#             return tel
#         else:
#             raise forms.ValidationError('手机号码不存在')
#
#
#     def clean(self):
#         #验证密码是否重复
#         #1.获取两次的密码数据
#         pwd=self.cleaned_data.get('newpassword1')
#         pwd1=self.cleaned_data.get('newrepassword2')
#         if pwd and pwd1 and pwd != pwd1:
#             raise forms.ValidationError('两次密码不一致')
#         else:
#             #返回清洁后的数据
#             return self.cleaned_data
#
#      def clean_password(self):
#         tel=self.cleaned_data.get('tel')
#         try:
#             user=MarkUser.objects.get(tel=tel)
#         except MarkUser.DoesNotExist:
#             raise forms.ValidationError({'tel':'手机号码错误'})
#
#         #验证密码md5正向不可逆所以验证密码必须给获取密码数据进行编码加密
#         h=hashlib.md5(self.cleaned_data.get('password').encode('utf-8'))
#         if user.password !=h.hexdigest():
#             raise forms.ValidationError({'password':'密码错误'})
#
#         else:
#             pass
class ForgetModelForm(forms.ModelForm):
    password = forms.CharField(max_length=16,
                               min_length=6,
                               # error_messages获取表单字段错误信息
                               error_messages={
                                   'required': '密码不能为空',
                                   'max_length': '最大长度为16位',
                                   'min_length': '最小长度为6位',
                               })  # CharField用于接收文本
    repassword = forms.CharField(error_messages={
        'required': '请确认密码',
    })

    class Meta:
        model = MarkUser
        fields = ['tel']
        error_messages = {
            'tel': {
                'required': '请输入手机号码'
            }
        }

    def clean_tel(self):
        # 验证手机号码是否重复
        # 获取清洁后的数据tel
        tel = self.cleaned_data.get('tel')
        # 去数据库查询数据是否存在
        tel_judge = MarkUser.objects.filter(tel=tel).exists()
        if  not tel_judge:
            raise forms.ValidationError('手机号码不存在')
        else:
            return tel_judge

    def clean_password(self):
        # 验证密码是否重复
        # 1.获取两次的密码数据
        pwd = self.cleaned_data.get('password')
        pwd1 = self.cleaned_data.get('repassword')
        if pwd and pwd1 and pwd != pwd1:
            raise forms.ValidationError('两次密码不一致')
        else:
            # 返回清洁后的数据
            return self.cleaned_data
