from django.db import models
import uuid
from master.models import *
from accounts.models import *
from tax_settings.models import *

# Create your models here.

WASHED_TRANSFER_CHOICES = (
        ('used','Used'),
        ('scrap', 'Scrap'),
    )

class ProdutItemMaster(models.Model):
    id   = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.CharField(max_length=20,  blank=True)
    created_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    
    product_name = models.CharField(max_length=50,unique=True)
    category = models.ForeignKey('master.CategoryMaster', on_delete=models.CASCADE,null=True,blank=True)
    unit_choices = (
        ('Pcs', 'Pcs'),
        ('Nos', 'Nos'),  # Added 'Nos' as an option
    )
    unit = models.CharField(max_length=50, choices=unit_choices, null=True, blank=True)
    tax = models.ForeignKey('tax_settings.Tax', on_delete=models.CASCADE, null=True, blank=True)
    rate = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    
    class Meta:
        ordering = ('product_name',)
    
    def __str__(self):
        return str(self.product_name)
    
class Product(models.Model):
    product_id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.CharField(max_length=20,  blank=True)
    created_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    
    product_name = models.ForeignKey(ProdutItemMaster, on_delete=models.CASCADE,null=True, blank=True)
    quantity=models.PositiveIntegerField(null=True, blank=True)
    branch_id = models.ForeignKey('master.BranchMaster', on_delete=models.CASCADE)
    fiveg_status = models.BooleanField(default=False)

    
    class Meta:
            ordering = ('created_date',)

    def __str__(self):
            return str(self.product_name.product_name)
    
class Product_Default_Price_Level(models.Model):
    def_price_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.CharField(max_length=20,  blank=True)
    created_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    CUSTOMER_TYPE_CHOICES = (
        ('HOME', 'HOME'),
        ('CORPORATE', 'CORPORATE'),
        ('SHOP', 'SHOP')
    )
    customer_type = models.CharField(max_length=100, choices=CUSTOMER_TYPE_CHOICES, null=True, blank=True)
    product_id = models.ForeignKey(ProdutItemMaster, on_delete=models.CASCADE, null=True, blank=True)
    rate = models.CharField(max_length=50)
    class Meta:
        ordering = ('customer_type',)

    def __str__(self):
        return str(self.customer_type)
    
class Staff_Orders(models.Model):
    staff_order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=30, null=True, blank=True, unique=True)
    created_by = models.CharField(max_length=20,  blank=True)
    created_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    C_STATUS = (
        ('Order Request', 'Order Request'),
        ('Cancelled', 'Cancelled'),
        ('Pending', 'Pending'),
        ('Delivered', 'Delivered'),
    )
    status = models.CharField(max_length=20, choices=C_STATUS, null=True, blank=True, default='Order Request')
    total_amount = models.CharField(max_length=20, null=True, blank=True)
    VIA_CHOICES = (
        ('Via App', 'Via App'),
        ('Via Staff', 'Via Staff'),
    )
    order_via = models.CharField(max_length=20, choices=VIA_CHOICES, null=True, blank=True, default='Via Staff')
    order_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ('order_number',)

    def __str__(self):
        return f'order number : {self.order_number}, created date : {self.created_date}, order date : {self.order_date}'
    
class Staff_Orders_details(models.Model):
    staff_order_details_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.CharField(max_length=20,  blank=True)
    created_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    staff_order_id =  models.ForeignKey(Staff_Orders, on_delete=models.SET_NULL, null=True, blank=True,related_name='staff_orders')
    product_id = models.ForeignKey(ProdutItemMaster, on_delete=models.SET_NULL, null=True, blank=True)
    C_STATUS = (
        ('Order Request', 'Order Request'),
        ('Cancelled', 'Cancelled'),
        ('Pending', 'Pending'),
        ('Delivered', 'Delivered'),
    )
    count = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    issued_qty = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    status = models.CharField(max_length=20, choices=C_STATUS, null=True, blank=True, default='Order Request')
    
    class Meta:
        ordering = ('staff_order_details_id',)

    def __str__(self):
        return str(self.staff_order_details_id)

class Staff_IssueOrders(models.Model):
    staff_issuesorder_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=30, null=True, blank=True, unique=True)
    salesman_id = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='salesman_orders',limit_choices_to={'designation_id__designation_name__in': ['Sales Executive', 'Sales Supervisor']})
    staff_Orders_details_id = models.ForeignKey(Staff_Orders_details, on_delete=models.SET_NULL, null=True, blank=True, related_name='salesman_order_details')
    van_route_id = models.ForeignKey('master.RouteMaster', on_delete=models.SET_NULL, null=True, blank=True, related_name='van_route_orders')
    product_id = models.ForeignKey(ProdutItemMaster, on_delete=models.CASCADE, related_name='issued_products')
    coupon_book= models.ForeignKey('coupon_management.NewCoupon',on_delete=models.SET_NULL, null=True, blank=True, related_name='couponsales')
    quantity_issued = models.CharField(max_length=50,null=True, blank=True)
    stock_quantity = models.CharField(max_length=50,null=True, blank=True)
    van = models.ForeignKey('van_management.Van', null=True, blank=True, on_delete=models.SET_NULL)

    STATUS_CHOICES = (
        ('Order Issued','Order Issued'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Order Issued')
    created_by = models.CharField(max_length=20,  blank=True)
    # created_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    class Meta:
            ordering = ('staff_issuesorder_id',)

    def __str__(self):
        return str(self.order_number)


class ProductStock(models.Model):
    product_stock_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.ForeignKey(ProdutItemMaster, on_delete=models.CASCADE,null=True, blank=True)
    quantity=models.PositiveIntegerField(null=True, blank=True)
    branch = models.ForeignKey('master.BranchMaster', on_delete=models.SET_NULL, null=True, blank=True,related_name='prod_stock_branch')
    status = models.BooleanField(default=False)
    created_by = models.CharField(max_length=20, blank=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('created_date',)

    def __str__(self):
        return str(self.product_name.product_name)

class DamageBottleStock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(ProdutItemMaster, on_delete=models.CASCADE,null=True, blank=True)
    quantity=models.PositiveIntegerField(default=0)
    
    created_by = models.CharField(max_length=20, blank=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('created_date',)

    def __str__(self):
        return str(self.product.product_name)
    
class ScrapProductStock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(ProdutItemMaster, on_delete=models.CASCADE,null=True, blank=True)
    quantity=models.PositiveIntegerField(default=0)
    
    created_by = models.CharField(max_length=20, blank=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('created_date',)

    def __str__(self):
        return str(self.product.product_name)
    
class WashingProductStock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(ProdutItemMaster, on_delete=models.CASCADE,null=True, blank=True)
    quantity=models.PositiveIntegerField(default=0)
    
    created_by = models.CharField(max_length=20, blank=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('created_date',)

    def __str__(self):
        return str(self.product.product_name)
    
class ScrapStock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(ProdutItemMaster, on_delete=models.CASCADE,null=True, blank=True)
    quantity=models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ('id',)

    def __str__(self):
        return str(self.product.product_name)
    
class WashingStock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(ProdutItemMaster, on_delete=models.CASCADE,null=True, blank=True)
    quantity=models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ('id',)

    def __str__(self):
        return str(self.product.product_name)
    
class WashedProductTransfer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(ProdutItemMaster, on_delete=models.CASCADE,null=True, blank=True)
    quantity=models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=WASHED_TRANSFER_CHOICES, default='used')
    
    created_by = models.CharField(max_length=20, blank=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('created_date',)

    def __str__(self):
        return str(self.product.product_name)
    
class WashedUsedProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(ProdutItemMaster, on_delete=models.CASCADE,null=True, blank=True)
    quantity=models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ('id',)

    def __str__(self):
        return str(self.product.product_name)
    
class ScrapcleanedStock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(ProdutItemMaster, on_delete=models.CASCADE,null=True, blank=True)
    quantity=models.PositiveIntegerField(default=0)
    
    created_by = models.CharField(max_length=20, blank=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('created_date',)

    def __str__(self):
        return str(self.product.product_name)