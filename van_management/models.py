from django.db import models
import uuid
from coupon_management.models import Coupon, CouponType, NewCoupon
from master.models import *
from product.models import Product, ProdutItemMaster

# Create your models here.
STOCK_TYPES = (
        ('opening_stock', 'Opening Stock'),
        ('change', 'Change'),
        ('return', 'Return'),
        ('closing', 'Closing'),
        ('damage', 'Damage'),
    )

class Van(models.Model):
    van_id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.CharField(max_length=20,  blank=True)
    created_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    van_make = models.CharField(max_length=50)
    plate = models.CharField(max_length=50)
    renewal_date = models.DateTimeField(blank=True, null=True)
    insurance_expiry_date = models.DateTimeField(blank=True, null=True)
    capacity = models.IntegerField(null=True,blank=True)
    driver = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True, blank=True,related_name='driver_van')
    salesman = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True, blank=True,related_name='salesman_van')
    branch_id = models.ForeignKey('master.BranchMaster', on_delete=models.SET_NULL, null=True, blank=True,related_name='van_branch')

    class Meta:
        ordering = ('van_make',)

    def __str__(self):
        return str(self.van_make)
    
class Van_Routes(models.Model):
    van_route_id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.CharField(max_length=20,  blank=True)
    created_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    van = models.ForeignKey(Van, on_delete=models.SET_NULL, null=True, blank=True,related_name='van_master')
    routes = models.ForeignKey(RouteMaster, on_delete=models.SET_NULL, null=True, blank=True,related_name='van_routes')

    class Meta:
        ordering = ('van',)

    def __str__(self):
        return str(self.van)

class Van_License(models.Model):
    van_license_id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.CharField(max_length=20,  blank=True)
    created_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    van = models.ForeignKey(Van, on_delete=models.SET_NULL, null=True, blank=True,related_name='van_license')
    emirate = models.ForeignKey(EmirateMaster, on_delete=models.SET_NULL, null=True, blank=True,related_name='license_emirate')
    license_no = models.CharField(max_length=50, null=True, blank=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('van',)

    def __str__(self):
        return str(self.van)


class ExpenseHead(models.Model):
    expensehead_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Expense(models.Model):
    expense_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expence_type = models.ForeignKey(ExpenseHead, on_delete=models.CASCADE)
    route = models.ForeignKey(RouteMaster, blank=True, null=True, on_delete=models.SET_NULL)
    van = models.ForeignKey(Van, null=True, blank=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.TextField(blank=True)
    expense_date = models.DateField()
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.expence_type} - {self.amount}"
    
class VanStock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.CharField(max_length=30, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True ,blank=True, null=True)
    
    van = models.ForeignKey(Van, on_delete=models.CASCADE)
    stock_type = models.CharField(max_length=100,choices=STOCK_TYPES)

    def __str__(self):
        return f"{self.id}"
    
    
class VanProductItems(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(ProdutItemMaster, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    van_stock = models.ForeignKey(VanStock, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}"
    
class VanCouponItems(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coupon = models.ForeignKey(NewCoupon, on_delete=models.CASCADE)
    book_no = models.CharField(max_length=100)
    coupon_type = models.ForeignKey(CouponType, on_delete=models.CASCADE)
    van_stock = models.ForeignKey(VanStock, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}"
    
class VanProductStock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(ProdutItemMaster, on_delete=models.CASCADE)
    stock_type = models.CharField(max_length=100,choices=STOCK_TYPES)
    count = models.PositiveIntegerField(default=0)
    van = models.ForeignKey(Van, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f"{self.id}"
    
class VanCouponStock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coupon = models.ForeignKey(NewCoupon, on_delete=models.CASCADE)
    stock_type = models.CharField(max_length=100,choices=STOCK_TYPES)
    count = models.PositiveIntegerField(default=0)
    van = models.ForeignKey(Van, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f"{self.id}"
    
    
class OffloadVan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    van = models.ForeignKey(Van, on_delete=models.CASCADE)
    product = models.ForeignKey(ProdutItemMaster, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    stock_type = models.CharField(max_length=100,choices=STOCK_TYPES)

    def __str__(self):
        return f"{self.id}"    
       
  
