from django import forms
from django.core.validators import RegexValidator

from user.helper import set_password
from user.models import SpUsers


class RegisterModelForm(forms.ModelForm):
    password=forms.CharField(max_length=16,
                             min_length=8,
                             error_messages={
                                 'required':'请填写密码',
                                 'min_length':'最小长度不少于8位',
                                 'max_length':'最大长度不高于16位',
                             })
    class Meta:
        #关联的模型名
        model=SpUsers
        #允许验证的表单字段名
        fields=['tel',]
        error_messages={
            "tel":{
                "required":"手机号码必须填写！"
            }
        }


    def clean_tel(self):
        #验证电话号码是否重复
        tel=self.cleaned_data.get('tel')
        flag=SpUsers.objects.filter(tel=tel).exists()
        if flag:
            raise forms.ValidationError("手机号码已经被注册")
        return tel

    def clean(self):
        pwd=self.cleaned_data.get('password')
        repwd=self.cleaned_data.get('repassword')

            # 确认密码错误
        if pwd and repwd and  pwd  !=  repwd:
            #确认密码错误
            raise forms.ValueError({"repassword":"两次密码不一致！"})
        #返回所有清洗后的数据
        return self.cleaned_data




class LoginModelForm(forms.ModelForm):
    class Meta:
        model = SpUsers
        fields = ['tel','password']

        error_messages = {
            'tel':{
                'required':'请填写手机号',
            },
            'password': {
                'required': '请填写密码',
            }
        }

    def clean(self):
        # 获取用户名和密码
        tel = self.cleaned_data.get('tel')
        password = self.cleaned_data.get('password')

        # 验证
        # 根据手机号码获取
        try:
            user = SpUsers.objects.get(tel=tel)
        except SpUsers.DoesNotExist:
            raise forms.ValidationError({'tel': '手机号错误'})

        # 验证密码
        if user.password != set_password(password):
            raise forms.ValidationError({'password': '密码填写6错误'})

        # 将用户信息保存到cleaned_data中
        self.cleaned_data['user'] = user
        return self.cleaned_data






