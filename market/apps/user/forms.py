from django import forms

from user.models import MarkUser


class RegisterModelForm(forms.ModelForm):
    password=forms.CharField(max_length=16,
                             min_length=6,
                             #error_messages获取表单字段错误信息
                             error_messages={
                                 'required':'密码不能为空',
                                 'max_length':'最大长度为16位',
                                 'min_length':'最小长度为6位',
                             })         # CharField用于接收文本
    repassword=forms.CharField(error_messages={
        'required':'请确认密码',
    })

    class Meta:
        #关联模型
        model=MarkUser
        #验证需要的字段
        fields=['tel',]
        error_messages={'tel':
                            {'required':'手机号码不能为空'}
                            }

    def clean_tel(self):
        #验证手机号码是否重复
        #获取清洁后的数据tel
        tel=self.cleaned_data.get('tel')
        #去数据库查询数据是否存在
        repeat_judge=MarkUser.objects.filter(tel=tel).exists()
        if repeat_judge:
            #抛出一个错误信息
            raise forms.ValidationError('手机号码已经注册')
        else:
            return tel

    def clean(self):
        #验证密码是否重复
        #1.获取两次的密码数据
        pwd=self.cleaned_data.get('password')
        pwd1=self.cleaned_data.get('repassword')
        if pwd and pwd1 and pwd != pwd1:
            raise forms.ValidationError('两次密码不一致')
        else:
            #返回清洁后的数据
            return self.cleaned_data



