from django.contrib import admin
from . models import *

# Register your models here.
admin.site.register(ProdutItemMaster)
admin.site.register(Product)
admin.site.register(ProductStock)
admin.site.register(Product_Default_Price_Level)