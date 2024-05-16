from django.contrib import admin

# Register your models here.
from . models import *

class CustomerCouponStockAdmin(admin.ModelAdmin):
    list_display = ('coupon_type_id', 'coupon_method', 'customer','count')
admin.site.register(CustomerCouponStock,CustomerCouponStockAdmin)

admin.site.register(CustomerCoupon)
admin.site.register(ChequeCouponPayment)

admin.site.register(CustomerOutstanding)
admin.site.register(OutstandingProduct)
admin.site.register(OutstandingAmount)
admin.site.register(OutstandingCoupon)
admin.site.register(CustomerOutstandingReport)

class CustomerSupplyAdmin(admin.ModelAdmin):
    list_display = ('id','customer','salesman','grand_total','discount','net_payable','vat','subtotal','amount_recieved')
admin.site.register(CustomerSupply,CustomerSupplyAdmin)
admin.site.register(CustomerSupplyItems)
admin.site.register(CustomerSupplyStock)