from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Van)
admin.site.register(Van_Routes)
admin.site.register(VanStock)
admin.site.register(VanProductItems)
admin.site.register(VanProductStock)
admin.site.register(VanCouponItems)
admin.site.register(VanCouponStock)