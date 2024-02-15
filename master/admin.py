from django.contrib import admin

from master.models import EmirateMaster

# Register your models here.
class EmiratesAdmin(admin.ModelAdmin):
    list_display = ['created_by','created_date','name']
admin.site.register(EmirateMaster,EmiratesAdmin)