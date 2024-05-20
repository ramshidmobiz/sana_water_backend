from datetime import datetime

from django import template
from django.db.models import Q, Sum,Subquery,Value
from django.db.models.functions import Coalesce

from accounts.models import CustomUser
from client_management.models import CustomerSupply, CustomerSupplyItems
from master.models import CategoryMaster
from product.models import Staff_IssueOrders, Staff_Orders_details
from van_management.models import Offload, Van, Van_Routes, VanProductItems, VanProductStock

register = template.Library()

@register.simple_tag
def get_empty_bottles(salesman):
    try:
        return CustomerSupply.objects.filter(salesman=salesman,created_date__date=datetime.today().date()).aggregate(total=Coalesce(Sum('collected_empty_bottle'), Value(0)))['total']
    except CustomerSupply.DoesNotExist:
        return 0
    
@register.simple_tag
def get_van_product_wise_stock(date,van,product):
    van = Van.objects.get(pk=van)
    van_poducts_items = VanProductItems.objects.filter(van_stock__van=van,product__pk=product)
    van_stock = VanProductStock.objects.filter(van=van,product__pk=product)
    
    if date:
        date = date
    else:
        date = datetime.today().date()
        
    staff_order_details = Staff_Orders_details.objects.filter(staff_order_id__created_date__date=date,product_id__pk=product,staff_order_id__created_by=van.salesman.pk)
    requested_count = staff_order_details.aggregate(total_count=Sum('count'))['total_count'] or 0
    issued_count = staff_order_details.aggregate(total_count=Sum('issued_qty'))['total_count'] or 0
    supply_instances = CustomerSupplyItems.objects.filter(product__pk=product,customer_supply__salesman=van.salesman,customer_supply__created_date__date=date)
    
    return{
        "opening_stock": van_poducts_items.filter(van_stock__created_date__date=date,van_stock__stock_type="opening_stock").aggregate(total_count=Sum('count'))['total_count'] or 0,
        "requested_count": requested_count,
        "issued_count": issued_count,
        "empty_bottle_collected": van_stock.filter(stock_type="emptycan").aggregate(total_count=Sum('count'))['total_count'] or 0,
        "sold_count": supply_instances.aggregate(total_count=Sum('quantity'))['total_count'] or 0,
        "return_count": van_stock.filter(stock_type="return").aggregate(total_count=Sum('count'))['total_count'] or 0,
        "closing_count": van_stock.filter(stock_type="closing").aggregate(total_count=Sum('count'))['total_count'] or 0,
        "change_count": van_stock.filter(stock_type="change").aggregate(total_count=Sum('count'))['total_count'] or 0,
        "offload_count": Offload.objects.filter(van=van,product__pk=product,created_date__date=date).aggregate(total_count=Sum('quantity'))['total_count'] or 0,
        "damage_count": van_stock.filter(stock_type="damage").aggregate(total_count=Sum('count'))['total_count'] or 0,
        "total_stock": van_stock.filter(stock_type__in=["opening_stock","closing"]).aggregate(total_count=Sum('count'))['total_count'] or 0,
    }
    
    
@register.simple_tag
def get_five_gallon_ratewise_count(rate,date,salesman):
    instances = CustomerSupplyItems.objects.filter(customer_supply__created_date__date=date,customer_supply__salesman_id=salesman,product__product_name="5 Gallon",customer_supply__customer__rate=rate)
    return {
        "debit_amount_count": instances.filter(customer_supply__customer__sales_type="CASH").count(),
        "credit_amount_count": instances.filter(customer_supply__customer__sales_type="CREDIT").count()
    }