import datetime

from django import template
from django.db.models import Q, Sum

from accounts.models import Customers
from master.functions import get_next_visit_date
from client_management.models import *
register = template.Library()

@register.simple_tag
def get_next_visit_day(customer_pk):
    customer = Customers.objects.get(pk=customer_pk)
    if not customer.visit_schedule is None:
        next_visit_date = get_next_visit_date(customer.visit_schedule)
        # customer.next_visit_date = next_visit_date
        return next_visit_date
    else:
      return None

@register.simple_tag
def bottle_stock(customer_pk):
    customer = Customers.objects.get(pk=customer_pk)
    
    total_bottle_count = CustomerSupply.objects.filter(customer=customer.customer_id)\
                                                    .aggregate(total_quantity=Sum('allocate_bottle_to_custody'))['total_quantity'] or 0
        
    last_supplied_count = CustomerSupplyItems.objects.filter(customer_supply__customer=customer.customer_id)\
                                                      .order_by('-customer_supply__created_date')\
                                                      .values_list('quantity', flat=True).first() or 0

    pending_count = CustomerSupply.objects.filter(customer=customer.customer_id)\
                                                   .aggregate(total_quantity=Sum('allocate_bottle_to_pending'))['total_quantity'] or 0

    final_bottle_count = total_bottle_count + last_supplied_count + pending_count 
    # print("final_bottle_count",final_bottle_count)
    
    return final_bottle_count