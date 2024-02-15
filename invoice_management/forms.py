from datetime import date
from django.forms.widgets import TextInput,Textarea,Select,DateInput,CheckboxInput,FileInput,PasswordInput
from django import forms

from master.models import CategoryMaster

from . models import *

class InvoiceForm(forms.ModelForm):
    customer_id = forms.CharField(widget=forms.TextInput(attrs={'type': 'hidden','name': 'customer_id','id':'customer_id_hfield'}))
    
    class Meta:
        model = Invoice
        fields = ['net_taxable','vat','amout_total','discount','amout_recieved','customer_id']
        
        widgets = {
            'net_taxable': TextInput(attrs={'class': 'required form-control text-right'}), 
            'vat': TextInput(attrs={'class': 'required form-control text-right'}), 
            'amout_total': TextInput(attrs={'class': 'required form-control text-right'}), 
            'discount': TextInput(attrs={'class': 'required form-control text-right'}), 
            'amout_recieved': TextInput(attrs={'class': 'required form-control text-right'}), 
        }
        
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        
    #     self.fields['created_date'].widget = forms.TextInput(attrs={
    #         'type': 'date',
    #         'class': 'required form-control',
    #         'placeholder': 'Enter Date',
    #         'value': date.today().strftime('%Y-%m-%d')
    #     })
        
        
class InvoiceItemsForm(forms.ModelForm):
    # category = forms.ModelChoiceField(
    #     queryset=CategoryMaster.objects.all(),
    #     widget=forms.Select(attrs={'class': 'required form-control product-category'})
    # )
    
    class Meta:
        model = InvoiceItems
        fields = ['product','rate','total_including_vat','qty','remarks','category']

        widgets = {
            'category': Select(attrs={'class': 'required form-control product-category'}), 
            'product': Select(attrs={'class': 'required form-control product-item'}), 
            'rate': TextInput(attrs={'class': 'required form-control','placeholder' : 'Enter Rate'}), 
            'qty': TextInput(attrs={'class': 'form-control product-qty','placeholder' : 'Enter QTY'}), 
            'total_including_vat': TextInput(attrs={'class': 'form-control total_including_vat','placeholder' : 'Enter Total'}), 
            'remarks': Textarea(attrs={'class': 'form-control','placeholder' : 'Serial Number Should be added here','rows':'2' }), 
        }
