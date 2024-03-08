import datetime

from django import template
from django.db.models import Q, Sum

from accounts.models import CustomUser
from van_management.models import Van_Routes

register = template.Library()

@register.simple_tag
def get_salesman_name(staff_id):
    try:
        # Ensure to sanitize and validate staff_id if needed
        salesman = CustomUser.objects.get(id=staff_id)
        return salesman.get_full_name()
    except CustomUser.DoesNotExist:
        return "--"
    
@register.simple_tag
def get_route_name(staff_id):
    try:
        return Van_Routes.objects.get(van__salesman__pk=staff_id)
    except :
        return "--"

