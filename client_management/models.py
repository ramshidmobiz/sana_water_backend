from django.db import models
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from accounts.models import *
from product.models import *
from django.http import HttpResponse


class Customer_Custody_Items(models.Model):
    DEPOSIT_TYPES = [
        ('cash', 'Cash Deposit'),
        ('cheque', 'Cheque Deposit'),
        ('other', 'Other Deposit'),
    ]
    custody_item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey('accounts.Customers', on_delete=models.SET_NULL, null=True, blank=True,related_name='customer_item')
    product = models.ForeignKey('product.Product', on_delete=models.SET_NULL, null=True, blank=True,related_name='cutomer_product')
    rate = models.CharField(max_length=50,null=True, blank=True)
    count = models.CharField(max_length=50,null=True, blank=True)
    amount = models.CharField(max_length=50,null=True, blank=True)
    created_by = models.CharField(max_length=20,  blank=True)
    created_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    modified_by = models.CharField(max_length=20, null=True, blank=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    empty_bottles = models.IntegerField(blank=True,null=True)
    cooler = models.IntegerField(blank=True,null=True)
    dispenser = models.IntegerField(blank=True,null=True)
    serialnumber = models.IntegerField(blank=True,null=True)
    deposit_type = models.CharField(max_length=10, choices=DEPOSIT_TYPES, blank=True, null=True)
    deposit_form_number = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey('master.CategoryMaster', on_delete=models.SET_NULL, null=True, blank=True)



    class Meta:
        ordering = ('customer',)

    def __str__(self):
        return str(self.customer)
def generate_pay_order(request, custody_item_id):
    custody_item = Customer_Custody_Items.objects.get(custody_item_id=custody_item_id)
    # Check if deposit type is set and generate pay order accordingly
    if custody_item.deposit_type:
        # Generate pay order logic based on the deposit type
        # This is just a placeholder example
        pay_order_content = f"Pay Order for {custody_item.deposit_type} deposit"
        return HttpResponse(pay_order_content)
    else:
        return HttpResponse("No deposit type set. Cannot generate pay order.")


def generate_invoice(request, custody_item_id):
    custody_item = Customer_Custody_Items.objects.get(custody_item_id=custody_item_id)
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