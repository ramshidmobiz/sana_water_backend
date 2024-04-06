import datetime

from django import template
from django.db.models import Q, Sum

from accounts.models import Customers
from master.functions import get_next_visit_date

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