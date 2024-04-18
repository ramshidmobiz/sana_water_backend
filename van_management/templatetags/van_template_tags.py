from datetime import datetime

from django import template
from django.db.models import Q, Sum,Subquery,Value
from django.db.models.functions import Coalesce

from accounts.models import CustomUser
from client_management.models import CustomerSupply
from master.models import CategoryMaster
from van_management.models import Van_Routes

register = template.Library()

@register.simple_tag
def get_empty_bottles(salesman):
    try:
        return CustomerSupply.objects.filter(salesman=salesman,created_date__date=datetime.today().date()).aggregate(total=Coalesce(Sum('collected_empty_bottle'), Value(0)))['total']
    except CustomerSupply.DoesNotExist:
        return 0

