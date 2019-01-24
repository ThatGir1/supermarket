from django.contrib import admin

# Register your models here.
from goods.models import Category, Goods_Spu, Unit, Goods_Sku, Album, Banner, Activity, ActivityZone

admin.site.register(Category),
admin.site.register(Goods_Spu),
admin.site.register(Unit),
admin.site.register(Goods_Sku),
admin.site.register( Album),
admin.site.register(Banner),
admin.site.register(Activity),
admin.site.register(ActivityZone),