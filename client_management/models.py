from django.db import models
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from accounts.models import *
from coupon_management.models import COUPON_METHOD_CHOICES, Coupon, CouponLeaflet, CouponType, NewCoupon
from product.models import *
from django.http import HttpResponse

COUPON_TYPE = (
    ('cash_coupon','Cash Coupon'),
    ('credit_coupon','Credit Coupon'),
)

PAYMENT_METHOD = (
    ('cash','Cash'),
    ('cheque','Cheque'),
)

DEPOSIT_TYPES = (
    ('deposit', 'Deposit'),
    ('non_deposit', 'Non Deposit'),
)

PRODUCT_TYPES = (
    ('amount','Amount'),
    ('emptycan','Emptycan'),
    ('coupons','Coupons'),
)

class CustodyCustom(models.Model):
    custody_custom_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey('accounts.Customers', on_delete=models.CASCADE,null=True,blank=True)
    agreement_no = models.CharField(max_length=20, null=True, blank=True)
    total_amount = models.IntegerField(blank=True,null=True)
    deposit_type = models.CharField(max_length=20,choices=DEPOSIT_TYPES,null=True,blank=True)
    
    created_by = models.CharField(max_length=20,  blank=True)
    created_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    modified_date = models.DateTimeField(blank=True, null=True)

class CustodyCustomItems(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    custody_custom = models.ForeignKey(CustodyCustom, on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey('product.ProdutItemMaster', on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.IntegerField(blank=True,null=True)
    serialnumber = models.CharField(max_length=20, null=True, blank=True)
    amount = models.IntegerField(blank=True,null=True)

    class Meta:
        ordering = ('custody_custom__created_date',)

    def __str__(self):
        return str(self.id)
    

class CustodyCustomDeposit(models.Model):
    DEPOSIT_TYPES = [
        ('cash', 'Cash Deposit'),
        ('cheque', 'Cheque Deposit'),
        ('other', 'Other Deposit'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    custody_custom = models.ForeignKey(CustodyCustom,on_delete=models.CASCADE,null=True,blank=True)
    deposit_type = models.CharField(max_length=10, choices=DEPOSIT_TYPES)
    deposit_form_number = models.CharField(max_length=100,)

    
class CustomerReturnReason(models.Model):
    reason_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reason =models.CharField(max_length=300)
   
    
    class Meta:
        db_table = 'customer_return_reason'
        verbose_name = ('Customer Return Reason')
        verbose_name_plural = ('Customer Return Reason')
    
    def _str_(self):
        return str(self.pk)
    

class CustomerReturn(models.Model):
    retutn_id = models.CharField(max_length=100)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
    count = models.IntegerField(blank=True,null=True)
    serialnumber = models.IntegerField(blank=True,null=True)
    amount = models.IntegerField(blank=True,null=True)
    deposit_form_number = models.CharField(max_length=100,default='')


    
    class Meta:
        db_table = 'customer_return_items'
        verbose_name = ('Customer Return Items')
        verbose_name_plural = ('Customer Return Items')
    
    def _str_(self):
        return str(self.pk)
    

def generate_pay_order(request, custody_item_id):
    custody_item = CustodyCustomItems.objects.get(custody_item_id=custody_item_id)
    # Check if deposit type is set and generate pay order accordingly
    if custody_item.deposit_type:
        # Generate pay order logic based on the deposit type
        # This is just a placeholder example
        pay_order_content = f"Pay Order for {custody_item.deposit_type} deposit"
        return HttpResponse(pay_order_content)
    else:
        return HttpResponse("No deposit type set. Cannot generate pay order.")


def generate_invoice(request, custody_item_id):
    custody_item = CustodyCustomItems.objects.get(custody_item_id=custody_item_id)
    # Check if deposit type is set and generate invoice accordingly
    if custody_item.deposit_type:
        # Generate invoice logic based on the deposit type
        # This is just a placeholder example
        invoice_content = f"Invoice for {custody_item.deposit_type} deposit"
        return HttpResponse(invoice_content)
    else:
        return HttpResponse("No deposit type set. Cannot generate invoice.")

class Customer_Inhand_Coupons(models.Model):
    cust_inhand_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey('accounts.Customers', on_delete=models.SET_NULL, null=True, blank=True,related_name='cust_coupon')
    no_of_coupons = models.CharField(max_length=20, null=True, blank=True)
    created_by = models.CharField(max_length=20,  blank=True)
    created_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    class Meta:
        ordering = ('customer',)

    def __str__(self):
        return str(self.customer)
    

class Vacation(models.Model):
    vacation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey('accounts.Customers', on_delete = models.SET_NULL, null = True)
    start_date = models.DateField()
    end_date = models.DateField()
    note = models.TextField(blank=True, null=True)
    created_by = models.CharField(max_length=30, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True ,blank=True, null=True)
    class Meta:
        ordering = ('start_date',)
    def __str__(self):
        return self.customer
    
@receiver(post_save, sender=Vacation)
def delete_expired_vacations(sender, instance, created, **kwargs):
    if not created:
        today = date.today()
        if instance.end_date < today:
            instance.delete()
                   
class CustomerCoupon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey('accounts.Customers',on_delete = models.CASCADE)
    coupon = models.ForeignKey(NewCoupon,on_delete = models.CASCADE)
    salesman = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_by = models.CharField(max_length=30, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True ,blank=True, null=True)
    class Meta:
        ordering = ('-created_date',)
    def __str__(self):
        return self.customer
    
    def get_available_coupon_count(self):
        return CouponLeaflet.objects.filter(coupon=self.coupon,used=False).count()
    
class CustomerCouponStock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coupon_type_id = models.ForeignKey(CouponType, on_delete=models.CASCADE)
    coupon_method = models.CharField(max_length=10,choices=COUPON_METHOD_CHOICES,default='manual')
    customer = models.ForeignKey('accounts.Customers',on_delete = models.CASCADE)
    count = models.PositiveIntegerField()
   
    class Meta:
        ordering = ('-id',)
        
    def __str__(self):
        return self.customer.customer_name
    
class CustomerCouponPayment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey('accounts.Customers',on_delete = models.CASCADE)
    customer_coupon = models.ForeignKey(CustomerCoupon, on_delete=models.CASCADE)
    coupon_type = models.CharField(max_length=100,choices=COUPON_TYPE)
    payment_type = models.CharField(max_length=100,choices=PAYMENT_METHOD,null=True,blank=True)
    
    grand_total = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    discount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    net_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    total_payeble = models.DecimalField(default=0, max_digits=10, decimal_places=2)
   
    class Meta:
        ordering = ('-id',)
        
    def __str__(self):
        return self.customer
    
class CashCouponPayment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_coupon_payment = models.ForeignKey(CustomerCouponPayment,on_delete = models.CASCADE)
    amount_recieved = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)
   
    class Meta:
        ordering = ('-id',)
        
    def __str__(self):
        return self.customer_coupon_payment
    
class ChequeCouponPayment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_coupon_payment = models.ForeignKey(CustomerCouponPayment,on_delete = models.CASCADE)
    bank = models.CharField(max_length=200)
    cheque = models.CharField(max_length=200)
    cheque_no = models.CharField(max_length=200)
    date = models.DateField()
   
    class Meta:
        ordering = ('-id',)
        
    def __str__(self):
        return self.customer_coupon_payment
    
class CustomerOutstanding(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey('accounts.Customers', on_delete=models.CASCADE)
    product_type = models.CharField(max_length=200, choices=PRODUCT_TYPES)
    created_by = models.CharField(max_length=30, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        ordering = ('-id',)
        
    def __str__(self):
        return str(self.product_type)

class OutstandingAmount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_outstanding = models.ForeignKey(CustomerOutstanding, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

    class Meta:
        ordering = ('-id',)
        
    def __str__(self):
        return str(self.id)

class OutstandingProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_outstanding = models.ForeignKey(CustomerOutstanding, on_delete=models.CASCADE)
    empty_bottle = models.IntegerField(default=0)

    class Meta:
        ordering = ('-id',)
        
    def __str__(self):
        return str(self.empty_bottle)
    
class OutstandingCoupon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coupon_type = models.ForeignKey(CouponType,on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    customer_outstanding = models.ForeignKey(CustomerOutstanding, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-id',)
        
    def __str__(self):
        return str(self.coupon_type)
    
class CustomerOutstandingReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_type = models.CharField(max_length=200, choices=PRODUCT_TYPES)
    value = models.IntegerField(default=0)
    customer = models.ForeignKey('accounts.Customers', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-id',)
        
    def __str__(self):
        return str(self.id)

class CustomerSupply(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        customer = models.ForeignKey('accounts.Customers',on_delete = models.CASCADE)
        salesman = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
        grand_total = models.DecimalField(default=0, max_digits=10, decimal_places=2)
        discount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
        net_payable = models.DecimalField(default=0, max_digits=10, decimal_places=2)
        vat = models.DecimalField(default=0, max_digits=10, decimal_places=2)
        subtotal = models.DecimalField(default=0, max_digits=10, decimal_places=2)
        amount_recieved = models.DecimalField(default=0, max_digits=10, decimal_places=2)
        collected_empty_bottle = models.PositiveIntegerField(default=0)
        allocate_bottle_to_pending = models.PositiveIntegerField(default=0)
        allocate_bottle_to_custody = models.PositiveIntegerField(default=0)
        allocate_bottle_to_paid = models.PositiveIntegerField(default=0)
        
        created_by = models.CharField(max_length=30, blank=True)
        created_date = models.DateTimeField(auto_now_add=True)
        modified_by = models.CharField(max_length=20, null=True, blank=True)
        modified_date = models.DateTimeField(auto_now=True ,blank=True, null=True)
        class Meta:
            ordering = ('-created_date',)
        def __str__(self):
            return self.customer

class CustomerSupplyItems(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        customer_supply = models.ForeignKey(CustomerSupply,on_delete = models.CASCADE)
        product = models.ForeignKey(ProdutItemMaster, on_delete=models.CASCADE,null=True,blank=True)
        quantity = models.PositiveIntegerField()
        amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)

        class Meta:
            ordering = ('-id',)
            
        def __str__(self):
            return self.customer_supply
        
class CustomerSupplyCoupon(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        customer_supply = models.ForeignKey(CustomerSupply,on_delete = models.CASCADE)
        leaf = models.ManyToManyField(CouponLeaflet)

        class Meta:
            ordering = ('-id',)
            
        def __str__(self):
            return self.customer_supply
        
class CustomerSupplyStock(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        product = models.ForeignKey(ProdutItemMaster, on_delete=models.CASCADE,null=True,blank=True)
        customer = models.ForeignKey('accounts.Customers',on_delete = models.CASCADE)
        stock_quantity = models.PositiveIntegerField(default=0)  

        class Meta:
            ordering = ('-id',)
            
        def __str__(self):
            return self.product
        





