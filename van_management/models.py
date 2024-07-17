from datetime import timedelta
import uuid

from django.db import models
from django.db.models import Sum

from master.models import *
from product.models import Product, ProdutItemMaster
from coupon_management.models import Coupon, CouponType, NewCoupon

# Create your models here.
STOCK_TYPES = (
        ('opening_stock', 'Opening Stock'),
        ('change', 'Change'),
        ('return', 'Return'),
        ('closing', 'Closing'),
        ('damage', 'Damage'),
        ('emptycan','Empty Can')
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
    bottle_count = models.PositiveIntegerField(default=0)
    driver = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True, blank=True,related_name='driver_van')
    salesman = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True, blank=True,related_name='salesman_van')
    branch_id = models.ForeignKey('master.BranchMaster', on_delete=models.SET_NULL, null=True, blank=True,related_name='van_branch')

    class Meta:
        ordering = ('van_make',)

    def __str__(self):
        return str(self.van_make)
    
    def get_total_vanstock(self,date):
        if date:
            date = datetime.strptime(date, '%Y-%m-%d').date()
        else:
            date = datetime.today().date()
        
        product_count = VanProductStock.objects.filter(created_date=date,van=self).aggregate(total_amount=Sum('stock'))['total_amount'] or 0
        coupon_count = VanCouponStock.objects.filter(created_date=date,van=self).aggregate(total_amount=Sum('stock'))['total_amount'] or 0
        return product_count + coupon_count
    
    def get_van_route(self):
        try:
            return Van_Routes.objects.filter(van=self).first().routes.route_name
        except:
            return "No Route Assigned"
    
    def get_vans_routes(self):
        van_route = Van_Routes.objects.filter(van=self).first()
        if van_route and van_route.routes:
            return van_route.routes.route_name
        return "No Route Assigned"
    
class Van_Routes(models.Model):
    van_route_id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.CharField(max_length=20,  blank=True)
    created_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    van = models.ForeignKey(Van, on_delete=models.CASCADE, null=True, blank=True,related_name='van_master')
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
    van = models.ForeignKey(Van, on_delete=models.CASCADE, null=True, blank=True,related_name='van_license')
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
    
# class VanProductStock(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     product = models.ForeignKey(ProdutItemMaster, on_delete=models.CASCADE)
#     stock_type = models.CharField(max_length=100,choices=STOCK_TYPES)
#     count = models.PositiveIntegerField(default=0)
#     van = models.ForeignKey(Van, on_delete=models.CASCADE,null=True,blank=True)

#     def __str__(self):
#         return f"{self.id}"

class VanProductStock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = models.DateField()
    opening_count = models.PositiveIntegerField(default=0)
    closing_count = models.PositiveIntegerField(default=0)
    change_count = models.PositiveIntegerField(default=0)
    damage_count = models.PositiveIntegerField(default=0)
    empty_can_count = models.PositiveIntegerField(default=0)
    return_count = models.PositiveIntegerField(default=0)
    requested_count = models.PositiveIntegerField(default=0)
    pending_count = models.PositiveIntegerField(default=0)
    sold_count = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    foc = models.PositiveIntegerField(default=0)
    
    product = models.ForeignKey(ProdutItemMaster,on_delete=models.CASCADE)
    van = models.ForeignKey(Van, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f"{self.id}"
    
    def save(self, *args, **kwargs):
        # offload_count = Offload.objects.filter(van=self.van,product=self.product,created_date__date=self.created_date).aggregate(total_count=Sum('quantity'))['total_count'] or 0
        # if self.stock > 0:
        self.closing_count = self.stock + self.empty_can_count + self.return_count
        
        super(VanProductStock, self).save(*args, **kwargs)
        
class VanCouponStock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = models.DateField()
    opening_count = models.PositiveIntegerField(default=0)
    closing_count = models.PositiveIntegerField(default=0)
    change_count = models.PositiveIntegerField(default=0)
    damage_count = models.PositiveIntegerField(default=0)
    return_count = models.PositiveIntegerField(default=0)
    requested_count = models.PositiveIntegerField(default=0)
    pending_count = models.PositiveIntegerField(default=0)
    sold_count = models.PositiveIntegerField(default=0)
    used_leaf_count = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    
    coupon = models.ForeignKey(NewCoupon, on_delete=models.CASCADE)
    van = models.ForeignKey(Van, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f"{self.id}"
    
    def save(self, *args, **kwargs):
        self.closing_count = self.stock + self.damage_count + self.return_count
        
        super(VanCouponStock, self).save(*args, **kwargs)
    
    
class Offload(models.Model): 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.CharField(max_length=30, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True ,blank=True, null=True)
    
    salesman = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    van = models.ForeignKey(Van, on_delete=models.CASCADE)
    product = models.ForeignKey(ProdutItemMaster, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    stock_type = models.CharField(max_length=100,choices=STOCK_TYPES)
    offloaded_date=models.DateField(blank=True, null=True)
    def __str__(self):
        return f"{self.id}"
    
class OffloadCoupon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.CharField(max_length=30, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True ,blank=True, null=True)
    
    salesman = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    van = models.ForeignKey(Van, on_delete=models.CASCADE)
    coupon = models.ForeignKey(NewCoupon, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    stock_type = models.CharField(max_length=100,choices=STOCK_TYPES)

    def __str__(self):
        return f"{self.id}"
    
class OffloadReturnStocks(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.CharField(max_length=30, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True ,blank=True, null=True)
    
    salesman = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    van = models.ForeignKey(Van, on_delete=models.CASCADE)
    product = models.ForeignKey(ProdutItemMaster, on_delete=models.CASCADE)
    scrap_count = models.PositiveIntegerField(default=0)
    washing_count = models.PositiveIntegerField(default=0)
    other_quantity= models.PositiveIntegerField(default=0)
    other_reason= models.CharField(max_length=300)
    def __str__(self):
        return f"{self.id}"
       
class SalesmanRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='salesman_requests_created')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    salesman = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='salesman_requests')
    request = models.TextField()

    def __str__(self):
        return f"{self.id}"
    

class BottleAllocation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.CharField(max_length=30, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True ,blank=True, null=True)
    
    route = models.ForeignKey(RouteMaster, blank=True, null=True, on_delete=models.SET_NULL)
    fivegallon_count = models.PositiveIntegerField(default=0)
    reason =models.CharField(max_length=300)


    def __str__(self):
        return f"{self.id}"

class StockMovement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=100, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True ,blank=True, null=True)
    
    salesman = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    from_van = models.ForeignKey(Van, on_delete=models.CASCADE,related_name='from_van')
    to_van = models.ForeignKey(Van, on_delete=models.CASCADE,related_name='to_van')


    def __str__(self):
        return f"{self.id}"
    
class StockMovementProducts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(ProdutItemMaster, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    stock_movement = models.ForeignKey(StockMovement, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.id}"
    
STOCK= (
    ('fresh','Fresh'),
    ('used','Used'),
)
    
class BottleCount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.CharField(max_length=100, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True ,blank=True, null=True)
    
    opening_stock = models.PositiveIntegerField(default=0)
    custody_issue = models.PositiveIntegerField(default=0)
    custody_return = models.PositiveIntegerField(default=0)
    qty_added = models.PositiveIntegerField(default=0)
    qty_deducted = models.PositiveIntegerField(default=0)
    closing_stock = models.PositiveIntegerField(default=0)
    comment = models.TextField()
    
    van = models.ForeignKey(Van,on_delete=models.CASCADE)
    
    class Meta:
        ordering = ('-created_date',)
        
    def save(self, *args, **kwargs):
        self.closing_stock = (
            self.opening_stock 
            + self.qty_added 
            + self.custody_return 
            - self.qty_deducted 
            - self.custody_issue
        )
        super(BottleCount, self).save(*args, **kwargs)
        
    def __str__(self):
        return str(self.id)
    
class EmptyCanStock(models.Model): 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(ProdutItemMaster, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    

    def __str__(self):
        return f"{self.id}" 
    
      
class OffloadRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    van = models.ForeignKey(Van, on_delete=models.CASCADE,null=True, blank=True)
    salesman = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    date=models.DateField(blank=True, null=True)
    
    created_by = models.CharField(max_length=20, blank=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('created_date',)

    def __str__(self):
        return str(self.van)
    
class OffloadRequestItems(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quantity = models.PositiveIntegerField(default=0)
    offloaded_quantity = models.PositiveIntegerField(default=0)
    stock_type = models.CharField(max_length=100)
    
    product = models.ForeignKey(ProdutItemMaster, on_delete=models.CASCADE,null=True, blank=True)
    offload_request = models.ForeignKey(OffloadRequest, on_delete=models.CASCADE,null=True, blank=True)
    
    class Meta:
        ordering = ('offload_request__created_date',)

    def __str__(self):
        return str(self.product.product_name)
    
class OffloadRequestReturnStocks(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    other_reason= models.CharField(max_length=300)
    scrap_count = models.PositiveIntegerField(default=0)
    washing_count = models.PositiveIntegerField(default=0)
    other_quantity= models.PositiveIntegerField(default=0)
    
    offload_request_item = models.ForeignKey(OffloadRequestItems, on_delete=models.CASCADE,null=True, blank=True)
    
    def __str__(self):
        return f"{self.id}"
    
class OffloadCoupon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quantity = models.PositiveIntegerField(default=0)
    stock_type = models.CharField(max_length=100,choices=STOCK_TYPES)
    
    coupon = models.ForeignKey(NewCoupon, on_delete=models.CASCADE)
    offload_request = models.ForeignKey(OffloadRequest, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}"