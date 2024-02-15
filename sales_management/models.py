from django.db import models

class OrderNumberField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 7)
        kwargs.setdefault('unique', True)
        kwargs.setdefault('editable', False)
        kwargs.setdefault('default', None)  # Add default value None
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if add and model_instance.order_number is None:  # Check if order_number is None
            last_order = model_instance._meta.model.objects.last()
            if last_order:
                last_order_number = int(last_order.order_number)
                model_instance.order_number = str(last_order_number + 1).zfill(7)
            else:
                model_instance.order_number = '2400000'  # Starting order number
        return super().pre_save(model_instance, add)
    
class SalesExtraModel(models.Model):
    qty_needed = models.IntegerField()
    no_of_coupons = models.IntegerField()
    coupon_variations = models.IntegerField()
    empty_bottles = models.IntegerField()
    collected_bottles = models.IntegerField()
    bottle_variations = models.IntegerField()
    # New status field with choices
    STATUS_CHOICES = (
        ('FOC', 'FOC'),
        ('PENDING', 'PENDING'),
        ('CUSTODY', 'CUSTODY'),
        ('PAID', 'PAID'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    order_number = OrderNumberField()

    def __str__(self):
        return f'SalesExtraModel {self.id}'
    
from django.db import models

class SalesTemp(models.Model):
    invoice_number = models.CharField(max_length=50) 
    data = models.JSONField()


class SaleEntryLog(models.Model):
    customer = models.ForeignKey('accounts.Customers', on_delete=models.CASCADE)
    last_delivery_date = models.DateField(null=True, blank=True)
    default_lt_bottle_count = models.IntegerField(null=True, blank=True)
    outstanding_coupons = models.IntegerField(null=True, blank=True, default=None)
    cash = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=None)
    empty_bottles = models.IntegerField(null=True, blank=True, default=None)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    net_taxable = models.DecimalField(max_digits=10, decimal_places=2)
    vat = models.DecimalField(max_digits=10, decimal_places=2)
    received_amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    coupon = models.ForeignKey('coupon_management.Coupon', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    extras = models.ForeignKey(SalesExtraModel, on_delete=models.CASCADE, null=True, blank=True)
    order_number = OrderNumberField()

    def __str__(self):
        return f'SaleEntryLog for {self.customer} - {self.last_delivery_date}'


class OutstandingLog(models.Model):
    customer = models.ForeignKey('accounts.Customers', on_delete=models.CASCADE)
    # sale_entry_log = models.ForeignKey(SaleEntryLog, on_delete=models.CASCADE)
    coupons = models.IntegerField(null=True)
    empty_bottles = models.IntegerField(null=True)
    cash = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL,null=True, blank=True)
    order_number = OrderNumberField()

    def __str__(self):
        return f"{self.customer} - {self.created_date}"


class Transaction(models.Model):
    TRANSACTION_CHOICES = [
        ('INCOME', 'INCOME'),
        ('EXPENSE', 'EXPENSE'),
    ]

    TRANSACTION_CATEGORIES = [
        ('FOC', 'FOC'),
        ('PENDING', 'PENDING'),
        ('CUSTODY', 'CUSTODY'),
        ('PAID', 'PAID'),
    ]
    customer = models.ForeignKey('accounts.Customers', on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=TRANSACTION_CHOICES)
    transaction_category = models.CharField(max_length=20, choices=TRANSACTION_CATEGORIES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_staff = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='transactions_created')
    created_at = models.DateTimeField(auto_now_add=True)
    invoice_number = models.CharField(max_length=100, unique=True)
    order_number = OrderNumberField()


