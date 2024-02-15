from django.db import models
import uuid
from accounts.models import *
from master.models import *
from product.models import *



# Create your models here.

class Customer_Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_id = models.ForeignKey('accounts.Customers', on_delete=models.SET_NULL, null=True, blank=True)
    order_number = models.CharField(max_length=30, null=True, blank=True, unique=True)
    item_name = models.CharField(max_length=20, null=True, blank=True)
    rate = models.IntegerField(default=0)  
    quantity = models.IntegerField(null=True, blank=True)
    total_amount = models.CharField(max_length=20, null=True, blank=True)
    noof_empty_bottles_returned = models.CharField(max_length=20, null=True, blank=True)
    required_emptybottles = models.BooleanField(default=False, null=True, blank=True)
    noof_empty_bottles_reqrd = models.CharField(max_length=20, null=True, blank=True)
    empty_bottle_amnt = models.CharField(max_length=20, null=True, blank=True)
    total_net_amnt = models.CharField(max_length=30, null=True, blank=True, unique=True)
    delivery_date = models.DateField(null=True, blank=True)
    payment_option = models.CharField(max_length=50, choices=[('online payment', 'Online payment'), ('cash on delivery', 'Cash on delivery')])
    created_by = models.CharField(max_length=20, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=True)
   
   
    class Meta:
        ordering = ('-created_date',)

    def __str__(self):
        return str(self.order_id)