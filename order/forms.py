from django import forms
from django.forms import ModelForm
from .models import  *
from accounts.models import CustomUser
from master.models import RouteMaster
from product.models import Product



# class Reason_Add_Form(forms.ModelForm):
#     class Meta:
#         model = Order_change_Reason
#         fields = ['reason_name']
#         widgets= {
#             'reason_name':forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
#         }

# class Reason_Edit_Form(forms.ModelForm):
#     class Meta:
#         model = Order_change_Reason
#         fields = ['reason_name']
#         widgets= {
#             'reason_name':forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
#         }



# class Order_change_Form(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['salesman'].queryset = CustomUser.objects.filter(user_type='Salesman')
#         self.fields['order'].queryset = Customer_Order.objects.all()
#         self.fields['reason'].queryset = Order_change_Reason.objects.all()

#     class Meta:
#         model = Order_change
#         fields = ['order', 'salesman', 'reason', 'note', 'changed_quantity', 'change_date']
#         widgets= {
#             'changed_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
#             'change_date': forms.DateInput(attrs={'class': 'form-control', 'type':'date'}),
#             'order': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
#             'salesman': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
#             'reason':forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
#             'note':forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
#         }


# class Order_change_Edit_Form(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['salesman'].queryset = CustomUser.objects.filter(user_type='Salesman')
#         self.fields['reason'].queryset = Order_change_Reason.objects.all()

#     class Meta:
#         model = Order_change
#         fields = [ 'salesman', 'reason', 'note', 'changed_quantity', 'change_date']
#         widgets= {
#             'changed_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
#             'change_date': forms.DateInput(attrs={'class': 'form-control', 'type':'date'}),
#             'salesman': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
#             'reason':forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
#             'note':forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
#         }


# # Return
# class Order_return_Form(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['salesman'].queryset = CustomUser.objects.filter(user_type='Salesman')
#         self.fields['order'].queryset = Customer_Order.objects.all()
#         self.fields['reason'].queryset = Order_change_Reason.objects.all()

#     class Meta:
#         model = Order_return
#         fields = ['order', 'salesman', 'reason', 'note', 'returned_quantity', 'return_date']
#         widgets= {
#             'returned_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
#             'return_date': forms.DateInput(attrs={'class': 'form-control', 'type':'date'}),
#             'order': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
#             'salesman': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
#             'reason':forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
#             'note':forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
#         }


# class Order_return_Edit_Form(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['salesman'].queryset = CustomUser.objects.filter(user_type='Salesman')
#         self.fields['reason'].queryset = Order_change_Reason.objects.all()

#     class Meta:
#         model = Order_return
#         fields = ['salesman', 'reason', 'note', 'returned_quantity', 'return_date']
#         widgets= {
#             'returned_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
#             'return_date': forms.DateInput(attrs={'class': 'form-control', 'type':'date'}),
#             'salesman': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
#             'reason':forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
#             'note':forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
#         }


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['driver'].queryset = CustomUser.objects.filter(user_type='Driver')
        self.fields['salesman'].queryset = CustomUser.objects.filter(user_type='Salesman')
        self.fields['route'].queryset = RouteMaster.objects.all()
        self.fields['product'].queryset = Product.objects.all()
    class Meta:
        model = Order
        fields = ['driver', 'route', 'product', 'quantity', 'salesman', 'order_date']
        widgets = {
            'driver': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'route': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'product': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'salesman': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'order_date': forms.DateInput(attrs={'class': 'form-control', 'required': 'true', 'type': 'date'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'required': 'true','type': 'number',}),
        }

class OrderUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    class Meta:
        model = Order
        fields = ['quantity', 'order_date']
        widgets = {
            'order_date': forms.DateInput(attrs={'class': 'form-control', 'required': 'true', 'type': 'date'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'required': 'true','type': 'number',}),
        }