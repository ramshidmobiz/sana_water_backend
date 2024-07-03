from datetime import datetime
from decimal import Decimal

from django import template
from django.db.models import Q, Sum,Subquery,Value
from django.db.models.functions import Coalesce

from accounts.models import CustomUser
from client_management.models import CustomerSupply, CustomerSupplyItems
from master.models import CategoryMaster
from product.models import Staff_IssueOrders, Staff_Orders_details
from van_management.models import Offload, Van, Van_Routes, VanCouponStock, VanProductItems, VanProductStock

register = template.Library()

@register.simple_tag
def get_empty_bottles(salesman):
    try:
        return CustomerSupply.objects.filter(salesman=salesman,created_date__date=datetime.today().date()).aggregate(total=Coalesce(Sum('collected_empty_bottle'), Value(0)))['total']
    except CustomerSupply.DoesNotExist:
        return 0
    
@register.simple_tag
def get_van_product_wise_stock(date,van,product):
    if VanProductStock.objects.filter(created_date=date,van=van,product__pk=product).exists():
        if date:
            date = datetime.strptime(date, '%Y-%m-%d').date()
        else:
            date = datetime.today().date()
            
        print(date)
            
        van = Van.objects.get(pk=van)
        van_stock = VanProductStock.objects.get(created_date=date,van=van,product__pk=product)
            
        staff_order_details = Staff_Orders_details.objects.filter(staff_order_id__created_date__date=date,product_id__pk=product,staff_order_id__created_by=van.salesman.pk)
        issued_count = staff_order_details.aggregate(total_count=Sum('issued_qty'))['total_count'] or 0
        
        total_stock = van_stock.stock + van_stock.opening_count
        sold_count = van_stock.sold_count
        offload_count = Offload.objects.filter(van=van,product__pk=product,created_date__date=date).aggregate(total_count=Sum('quantity'))['total_count'] or 0
        
        return {
            "opening_stock": van_stock.opening_count,
            "requested_count": Staff_Orders_details.objects.filter(product_id__pk=product,staff_order_id__created_date__date=date,created_by=van.salesman.pk).aggregate(total_count=Sum('count'))['total_count'] or 0,
            "issued_count": issued_count,
            "empty_bottle_collected": van_stock.empty_can_count,
            "return_count": van_stock.return_count,
            "sold_count": sold_count,
            "closing_count": van_stock.closing_count,
            "offload_count": offload_count,
            "change_count": van_stock.change_count,
            "damage_count": van_stock.damage_count,
            "total_stock": total_stock
        }
    
@register.simple_tag
def get_five_gallon_ratewise_count(rate,date,salesman):
    instances = CustomerSupplyItems.objects.filter(customer_supply__created_date__date=date,customer_supply__salesman_id=salesman,product__product_name="5 Gallon",customer_supply__customer__rate=rate)
    return {
        "debit_amount_count": instances.filter(customer_supply__amount_recieved__gt=0).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0,
        "credit_amount_count": instances.filter(customer_supply__amount_recieved=0).exclude(customer_supply__customer__sales_type__in=["FOC","CASH COUPON"]).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0,
        "coupon_amount_count": instances.filter(customer_supply__customer__sales_type="CASH COUPON").aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
    }
    
@register.simple_tag
def get_coupon_vanstock_count(van_pk,date,coupon_type):
    return VanCouponStock.objects.filter(created_date=date,van__pk=van_pk,coupon__coupon_type__coupon_type_name=coupon_type).aggregate(total_stock=Sum('stock'))['total_stock'] or 0
    

@register.simple_tag
def get_van_coupon_wise_stock(date, van, coupon):
    if VanCouponStock.objects.filter(created_date=date, van=van, coupon__pk=coupon).exists():
        if date:
            date = datetime.strptime(date, '%Y-%m-%d').date()
        else:
            date = datetime.today().date()

        van = Van.objects.get(pk=van)
        van_stock = VanCouponStock.objects.get(created_date=date, van=van, coupon__pk=coupon)

        staff_order_details = Staff_Orders_details.objects.filter(
            staff_order_id__created_date__date=date,
            product_id__pk=coupon,
            staff_order_id__created_by=van.salesman.pk
        )
        issued_count = staff_order_details.aggregate(total_count=Sum('issued_qty'))['total_count'] or 0

        total_stock = van_stock.stock + van_stock.opening_count
        sold_count = van_stock.sold_count
        offload_count = Offload.objects.filter(
            van=van,
            product__pk=coupon,
            created_date__date=date
        ).aggregate(total_count=Sum('quantity'))['total_count'] or 0

        return {
            "opening_stock": van_stock.opening_count,
            "requested_count": Staff_Orders_details.objects.filter(
                product_id__pk=coupon,
                staff_order_id__created_date__date=date,
                created_by=van.salesman.pk
            ).aggregate(total_count=Sum('count'))['total_count'] or 0,
            "issued_count": issued_count,
            "return_count": van_stock.return_count,
            "sold_count": sold_count,
            "closing_count": van_stock.closing_count,
            "offload_count": offload_count,
            "change_count": van_stock.change_count,
            "damage_count": van_stock.damage_count,
            "total_stock": total_stock
        }
    return {}