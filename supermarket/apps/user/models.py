from django.core.validators import RegexValidator
from django.db import models
from db.base_model import BaseModel

# Create your models here.

# Id 主键
# 	Create_time 创建时间	datetime（用户注册的时间）
# 	Update_time 更新时间 datetime  （用户修改信息的时间）
# 	Is_delete 是否删除  boolean		（假删除）
# 	Nickname 用户名	varchar
# 	Telephone 手机号	varchar
# 	Password	密码	varchar 	(哈希加密)
# 	Gender		性别	choice		(男， 女， 保密)
# 	Birthday	生日	datetime
# 	School		学校	varchar
# 	Location	地址	varchar
# 	Hometown	地址	varchar




class SpUsers(BaseModel):
    sex_choices = (
        (1, "男"),
        (2, "女"),
    )
    tel=models.CharField(max_length=11,
                         verbose_name="手机号码",
                         validators=[
                             RegexValidator(r'^1[3-9]\d{9}',"手机号码格式错误")
                         ])

    nickname=models.CharField(max_length=50,
                              null=True,
                              blank=True,
                              verbose_name="昵称")

    password=models.CharField(max_length=32,
                              verbose_name="密码")

    gender = models.SmallIntegerField(choices=sex_choices,
                                      default=1,
                                      verbose_name="性别"
                                      )

    school_name = models.CharField(max_length=50,
                                   null=True,
                                   blank=True,
                                   verbose_name="学校"
                                   )

    hometown = models.CharField(max_length=50,
                                null=True,
                                blank=True,
                                verbose_name="家乡"
                                )

    birth_date = models.DateField(null=True,
                                     blank=True,
                                     verbose_name="出生日期"
                                     )

    address = models.CharField(max_length=255,
                               null=True,
                               blank=True,
                               verbose_name="详细位置"
                               )






