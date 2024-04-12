from django.contrib import admin
from . models import *

# Register your models here.
class NewCouponAdmin(admin.ModelAdmin):
    list_display = ('coupon_id','coupon_type','book_num','no_of_leaflets','valuable_leaflets','free_leaflets','branch_id','status','coupon_method')
admin.site.register(NewCoupon,NewCouponAdmin)