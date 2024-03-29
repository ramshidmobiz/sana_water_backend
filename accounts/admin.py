from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'created_date', 'custom_id')
    ordering = ('-created_date',)
admin.site.register(Customers,CustomersAdmin)
