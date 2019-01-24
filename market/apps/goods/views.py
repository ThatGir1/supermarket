from django.shortcuts import render

# Create your views here.
from django.views import View

from db.base_view import VerifyLoginView
from goods.models import Goods_Spu, Goods_Sku, Category


class IndexView(VerifyLoginView):
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
    def get(self,request):
        # 查询所有的分类
        categorys = Category.objects.filter(is_delete=False)
        # 查询所有的商品
        goods_skus = Goods_Sku.objects.filter(is_delete=False)

        context = {
            'categorys': categorys,
            'goods_skus': goods_skus,
        }

        return  render(request,'goods/category.html',context=context)

    def post(self,request):
        pass


class ListView(View):
    def get(self,request):
        return render(request,'goods/list.html')


    def post(self,request):
        pass

