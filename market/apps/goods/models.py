from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from db.model_base import BaseModel

is_on_sale_choices = (
    (False, "下架"),
    (True, "上架"),
)

class Category(BaseModel):
    """商品分类表"""
    cate_name=models.CharField(verbose_name='分类名称',
                              max_length=20
    )
    brief = models.CharField(verbose_name='描述',
                             max_length=200,
                             null=True,
                             blank=True
                             )


    def __str__(self):
        return self.cate_name

    class Meta:
        verbose_name = "商品分类管理"
        verbose_name_plural = verbose_name


class Goods_Spu(BaseModel):
    """商品Spu表"""
    spu_name = models.CharField(verbose_name='商品SPU名称',
                                max_length=20, )
    #将之前详情修改使用富文本
    spu_detail = RichTextUploadingField(verbose_name='商品详情')

    def __str__(self):
        return self.spu_name

    class Meta:
        verbose_name = "商品SPU"
        verbose_name_plural = verbose_name


class Unit(BaseModel):
    """商品单位表"""
    unit_name=models.CharField(max_length=20,
                            verbose_name='单位名')

    def __str__(self):
        return self.unit_name

    class Meta:
        verbose_name="商品单位管理"
        verbose_name_plural=verbose_name

class Goods_Sku(BaseModel):
    """商品SKU表"""
    sku_name=models.CharField(max_length=100,
                              verbose_name='商品sku名称')

    brief=models.CharField(max_length=200,
                           null=True,
                           blank=True,
                           verbose_name='商品简介')

    price=models.DecimalField(max_digits=9,
                              decimal_places=2,
                              default=0,
                              verbose_name='价格')

    unit=models.ForeignKey(to="Unit",verbose_name="单位")

    stock=models.IntegerField(default=0,
                              verbose_name='库存')

    salesvolume=models.IntegerField(default=0,
                                    verbose_name='销量')

    #默认相册第一张作为封面图片
    logo=models.ImageField(upload_to='goods/%Y%m/%d',
                           verbose_name='封面图片')

    is_on_sale=models.BooleanField(choices=is_on_sale_choices,
                                   default=False,
                                   verbose_name='是否上架')
    category=models.ForeignKey(to="Category" ,
                                verbose_name='商品分类id')

    goods_spu=models.ForeignKey(to="Goods_Spu",
                                verbose_name='商品Spuid')

    def __str__(self):
        return self.sku_name

    class Meta:
        verbose_name = "商品SKU管理"
        verbose_name_plural = verbose_name


class Album(BaseModel):
    """商品相册表"""
    img_url=models.ImageField(upload_to='goods_gallery/%Y%m/%d',
                              verbose_name='相册地址'
                              )

    goods_sku=models.ForeignKey(to='Goods_Sku')

    class Meta:
        verbose_name = "商品相册管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "商品相册:{}".format(self.img_url.name)


class Banner(BaseModel):
    """首页轮播表"""
    name= models.CharField(verbose_name="轮播活动名",
                            max_length=150,
                            )

    img_url = models.ImageField(verbose_name='轮播图片地址',
                                upload_to='banner/%Y%m/%d'
                                )

    order = models.SmallIntegerField(verbose_name="排序",
                                     default=0,
                                     )

    goods_sku = models.ForeignKey(to="Goods_Sku", verbose_name="商品SKU")

    class Meta:
        verbose_name = "轮播管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Activity(BaseModel):
    """首页活动表"""
    title = models.CharField(verbose_name='活动名称',
                             max_length=150)

    img_url = models.ImageField(verbose_name='活动图片地址',
                                upload_to='activity/%Y%m/%d'
                                )
    url_site = models.URLField(verbose_name='活动的url地址',
                               max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "活动管理"
        verbose_name_plural = verbose_name


class ActivityZone(BaseModel):
    """
        首页活动专区
    """
    title = models.CharField(verbose_name='活动专区名称', max_length=150)
    brief = models.CharField(verbose_name="活动专区的简介",
                             max_length=200,
                             null=True,
                             blank=True,
                             )

    order = models.SmallIntegerField(verbose_name="排序",
                                     default=0,
                                     )

    is_on_sale = models.BooleanField(verbose_name="是否上线",
                                     choices=is_on_sale_choices,
                                     default=0,
                                     )

    goods_sku = models.ManyToManyField(to="Goods_Sku",verbose_name="商品")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "活动专区管理"
        verbose_name_plural = verbose_name










