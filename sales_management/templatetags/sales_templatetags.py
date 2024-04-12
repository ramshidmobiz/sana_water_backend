import datetime

from django import template
from django.db.models import Q, Sum

register = template.Library()

# @register.simple_tag
# def get_salesman_name(staff_id):
#     try:
#         # Ensure to sanitize and validate staff_id if needed
#         salesman = CustomUser.objects.get(id=staff_id)
#         return salesman.get_full_name()
#     except CustomUser.DoesNotExist:
#         return "--"