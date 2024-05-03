from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Van)
admin.site.register(Van_Routes)
admin.site.register(VanStock)
admin.site.register(VanProductItems)
admin.site.register(VanCouponItems)

class VanProductStockAdmin(admin.ModelAdmin):
    list_display = ('product','stock_type','count','van')
admin.site.register(VanProductStock,VanProductStockAdmin)
class VanCouponStockAdmin(admin.ModelAdmin):
    list_display = ('van','coupon','stock_type','count')
admin.site.register(VanCouponStock,VanCouponStockAdmin)