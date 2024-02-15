from django import forms
from django.forms import ModelForm
from .models import *
from master.models import *


class Products_Create_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['unit'].choices = [
            (choice[0], choice[1]) for choice in self.fields['unit'].choices]
        self.fields['category_id'].queryset = CategoryMaster.objects.filter()


    class Meta:
        model = Product
        fields = ['product_name', 'unit', 'rate', 'category_id', 'tax']
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'unit': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'rate': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'category_id' : forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'tax' : forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
        }

class Products_Edit_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = Product
        fields = ['product_name', 'rate', 'category_id', 'tax']
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'rate': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'category_id' : forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'tax' : forms.Select(attrs={'class': 'form-control', 'required': 'true'}),

        }

class Defaultprice_Create_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = Product_Default_Price_Level
        fields = ['product_id', 'customer_type', 'rate']
        widgets = {
            'product_id': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'customer_type': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'rate': forms.TextInput(attrs={'class': 'form-control'})
        }


class Defaultprice_Edit_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    class Meta:
        model = Product_Default_Price_Level
        fields = ['customer_type', 'rate']
        widgets = {
            'customer_type': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'rate' : forms.TextInput(attrs={'class': 'form-control', 'required': 'true'})
        }

class StaffIssueOrdersForm(forms.ModelForm):
    class Meta:
        model = Staff_IssueOrders
        # fields = ['order_number', 'salesman_id', 'staff_Orders_details_id', 'van_route_id', 'product_id', 'quantity_issued', 'status']
        fields = ['quantity_issued','van_route_id','salesman_id']

        widgets = {
            # 'order_number': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'salesman_id': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            # 'staff_Orders_details_id': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'van_route_id': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            # 'product_id': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'quantity_issued': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            # 'status': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
        }
