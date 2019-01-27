from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from cart.hepler import json_msg, get_cart_count
from db.base_view import VerifyLoginView
from goods.models import Goods_Sku
from django_redis import get_redis_connection


class AddCartView(VerifyLoginView):
    """操作购物车, 添加购物车数据"""
    """
        1. 需要接收的参数
            sku_id count 
            从session中获取用户id

        2. 验证参数合法性
            a. 判断 为整数
            b. 要在数据库中存在商品
            c. 验证库存是否充足

        3. 操作数据库
            将购物车 保存到redis
            存储的时候采用的数据库类型为hash
            key           field value  field value
            cart_user_id  sku_id count

    """

    def post(self, request):
        # 1. 接收参数
        user_id = request.session.get("ID")
        sku_id = request.POST.get("sku_id")
        count = request.POST.get("count")

        # a.判断为整数
        try:
            sku_id = int(sku_id)
            count = int(count)
        except:
            return JsonResponse(json_msg(1, "参数错误!"))
        # b.要在数据库中存在商品
        try:
            goods_sku = Goods_Sku.objects.get(pk=sku_id)
        except Goods_Sku.DoesNotExist:
            return JsonResponse(json_msg(2, "商品不存在!"))

        # 判断库存
        if goods_sku.stock < count:
            return JsonResponse(json_msg(3, "库存不足!"))

        # 2. 操作数据
        # 创建连接
        r = get_redis_connection()
        # 处理购物车的 key
        cart_key = f"cart_{user_id}"

        # 添加
        # 获取购物车中已经存在的数量 加 上 需要添加 与 库存进行比较
        old_count = r.hget(cart_key, sku_id)  # 二进制
        if old_count is None:
            old_count = 0
        else:
            old_count = int(old_count)

        if goods_sku.stock < old_count + count:
            return JsonResponse(json_msg(3, "库存不足!"))

        # 将商品添加到购物车
        # r.hset(cart_key,sku_id,old_count + count)
        # ctrl + shift + u
        r.hincrby(cart_key, sku_id, count)

        # 获取购物车中的总数量
        cart_count = get_cart_count(request)

        # 3. 合成响应
        return JsonResponse(json_msg(0, "添加购物车成功", data=cart_count))
