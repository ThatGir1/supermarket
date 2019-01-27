from django.shortcuts import render

# Create your views here.
from django.views import View

from db.base_view import VerifyLoginView
from goods.models import Goods_Spu, Goods_Sku, Category


class IndexView(View):
    def get(self,request):
        return render(request,'goods/index.html')

    def post(self,request):
        pass

class DetailView(View):
    def get(self,request,id):
        #获取商品sku的信息
        goods_sku=Goods_Sku.objects.get(pk=id)

        #渲染页面
        context={
            'goods_sku':goods_sku,
        }

        return render(request,'goods/detail.html',context=context)

    def post(self,request):
        pass

class CategoryView(View):
    """
            1. 页面刚加载的时候 显示的商品只 显示 排序 排第一的分类下的商品
            2. 点击哪个分类 就显示 对应分类下的商品
            3. 可以按照 销量,价格(降,升),添加时间,综合(pk) 排序 并且 是对应分类下的商品
                添加一个参数order:
                    0: 综合
                    1: 销量降
                    2: 价格升
                    3: 价格降
                    4: 添加时间降
                order_rule = ['pk', '-sale_num', 'price', '-price', '-create_time']
        """

    def get(self,request,cate_id,order):
        # 查询所有的分类
        categorys = Category.objects.filter(is_delete=False)
        #取出第一个分类
        # categorys.first()
        if cate_id == "" :
            category=categorys.first()
            cate_id=category.pk
        else:
            #根据分类id查询对应id
            cate_id=int(cate_id)
            category = Category.objects.get(pk=cate_id)
        # 查询所有的商品
        goods_skus = Goods_Sku.objects.filter(is_delete=False,category=category)
        if order == "":
            order = 0
        order = int(order)

        order_rule = ['pk', '-salesvolume', 'price', '-price', '-create_time']
        goods_skus = goods_skus.order_by(order_rule[order])

        # if order ==0:
        #     goods_skus=goods_skus.oder_by("pk")
        #
        # elif order ==1:
        #     goods_skus=goods_skus.order_by("-salesvolume")
        #
        #
        # elif order == 2:
        #     goods_skus = goods_skus.order_by("price")
        #
        # elif order == 3:
        #     goods_skus = goods_skus.order_by("-price")
        #
        # elif order == 4:
        #     goods_skus = goods_skus.order_by("-create_time")

        context = {
            'categorys': categorys,
            'goods_skus': goods_skus,
            'cate_id':cate_id,
            "order":order,
        }

        return  render(request,'goods/category.html',context=context)

    def post(self,request):
        pass


class ListView(View):
    def get(self,request):
        return render(request,'goods/list.html')


    def post(self,request):
        pass

