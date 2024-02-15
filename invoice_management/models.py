import uuid
from django.db import models

from accounts.models import Customers
from master.models import CategoryMaster
from product.models import Product

# Create your models here.
INVOICE_TYPES = (
    ('cash_invoice', 'Cash Invoice'),
    ('credit_invoive', 'Credit Invoice'),
)

class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice_no = models.CharField(max_length=200)
    invoice_type = models.CharField(max_length=200, choices=INVOICE_TYPES,default='cash_invoice')
    created_date = models.DateTimeField()
    net_taxable = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    vat = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    discount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    amout_total = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    amout_recieved = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'invoice'
        verbose_name = ('Invoice')
        verbose_name_plural = ('Invoice')
    
    def __str__(self):
        return f'{self.id}'
    
    
class InvoiceItems(models.Model):
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    total_including_vat = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    remarks = models.TextField()
    is_deleted = models.BooleanField(default=False)
    
    category = models.ForeignKey(CategoryMaster, on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'invoice_items'
        verbose_name = ('Invoice Items')
        verbose_name_plural = ('Invoice Items')
    
    def __str__(self):
        return str(self.invoice.invoice_no)