from django import forms
from django.forms import ModelForm
from .models import *
from accounts.models import Customers
from django.db.models import Q
from django.core.validators import MinValueValidator
from django.utils import timezone


class Vacation_Add_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['customer'].queryset = Customers.objects.all()
        
    class Meta:
        model = Vacation
        fields = ['customer', 'start_date','end_date','note']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'required': True, 'type': 'date', 'min':timezone.now().date()}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'required': True, 'type': 'date', 'min':timezone.now().date()}),
            'note' : forms.TextInput(attrs={'class':'form-control'})
        }

class Vacation_Edit_Form(forms.ModelForm):
    class Meta:
        model = Vacation
        fields = [ 'start_date', 'end_date', 'note']
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'required': True, 'type': 'date', 'min':timezone.now().date()}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'required': True, 'type': 'date', 'min':timezone.now().date()}),
            'note': forms.TextInput(attrs={'class': 'form-control'})
        }

class CustomerSearchForm(forms.Form):
    search_query = forms.CharField(label='Search')

from master.models import RouteMaster

class CustodyItemFilterForm(forms.Form):
    route_name = forms.ModelChoiceField(
        queryset=RouteMaster.objects.all(),
        empty_label="All Routes",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'required': 'true'})
    )


from django import forms
from product.models import Product
from master.models import CategoryMaster
from django import forms
from .models import Customer_Custody_Items
class CustomerCustodyItemsForm(forms.ModelForm):
    class Meta:
        model = Customer_Custody_Items
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


# class ProductForm(forms.ModelForm):
#     category = forms.ModelChoiceField(
#         queryset=CategoryMaster.objects.all(),
#         label='Category',
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )
#     product_name = forms.ModelChoiceField(
#         queryset=Product.objects.none(), 
#         label='Product',
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )
#     serial_number = forms.IntegerField(
#         label='Serial Number',
#         widget=forms.NumberInput(attrs={'class': 'form-control'})
#     )
#     quantity = forms.IntegerField(
#         label='Quantity',
#         widget=forms.NumberInput(attrs={'class': 'form-control'})
#     )
#     rate = forms.IntegerField(
#         label='Rate',
#         widget=forms.NumberInput(attrs={'class': 'form-control'})
#     )
   
#     class Meta:
#         model = Product
#         fields = ['category', 'product_name','quantity','rate', 'serial_number']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if 'category' in self.data:
#             try:
#                 category_id = int(self.data.get('category'))
#                 self.fields['product_name'].queryset = Product.objects.filter(category_id=category_id).order_by('product_name')
#                 self.fields['rate'].queryset = Product.objects.filter(category_id=category_id).order_by('rate')

#             except (ValueError, TypeError):
#                 pass
#         elif self.instance.category_id is not None:
#             self.fields['product_name'].queryset = self.instance.category_id.product_set.order_by('product_name')
#         else:
#             self.fields['product_name'].queryset = Product.objects.none()

