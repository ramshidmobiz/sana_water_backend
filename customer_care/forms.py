from django import forms
from django.forms import ModelForm
from .models import *
from master.models import *
from client_management.models import *

class RequestType_Create_Form(forms.ModelForm):
    class Meta:
        model = RequestTypeMaster
        fields = ['request_name']
        widgets = {
            'request_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
        }

class RequestType_Edit_Form(forms.ModelForm):

    class Meta:
        model = RequestTypeMaster
        fields = ['request_name']
        widgets = {
            'request_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
        }


class CustomercreateForms(forms.ModelForm):
    def __init__(self,branch, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sales_staff'].queryset = CustomUser.objects.filter(is_active = True,branch_id = branch,designation_id__designation_name = "Sales Executive")
        self.fields['routes'].queryset = RouteMaster.objects.filter(branch_id = branch)
        self.fields['location'].queryset = LocationMaster.objects.filter(branch_id = branch)

    class Meta:
        model = Customers
        fields = ['customer_name','building_name','door_house_no','floor_no','sales_staff','routes','location','mobile_no','whats_app','email_id','gps_latitude','gps_longitude','customer_type','sales_type','no_of_bottles_required','max_credit_limit','credit_days','no_of_permitted_invoices']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'building_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'door_house_no': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'floor_no': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'sales_staff': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'routes': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'location': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'mobile_no': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'whats_app': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'email_id': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'gps_latitude': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'gps_longitude': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'customer_type': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'sales_type': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'no_of_bottles_required': forms.TextInput(attrs={'class': 'form-control', 'required': 'true','type':'number'}),
            'max_credit_limit': forms.TextInput(attrs={'class': 'form-control', 'required': 'true','type':'number'}),
            'credit_days': forms.TextInput(attrs={'class': 'form-control', 'required': 'true','type':'number'}),
            'no_of_permitted_invoices': forms.TextInput(attrs={'class': 'form-control', 'required': 'true','type':'number'}),
        }


class CreateRequestTypeForm(forms.ModelForm):
    class Meta:
        model=RequestTypeMaster
        fields=[
            'request_type','request_name'
            ]
        widgets = {
            'request_type': forms.Select(attrs={'class': 'form-control'}),
            'request_name': forms.Select(attrs={'class': 'form-control'})
        }
class ChangeofaddressForm(forms.ModelForm):
    def __init__(self,branch, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['routes'].queryset = RouteMaster.objects.filter(branch_id = branch)
        self.fields['location'].queryset = LocationMaster.objects.filter(branch_id = branch)

    class Meta:
        model = Customers
        fields = ['customer_name','location','building_name','door_house_no','floor_no','routes']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'location': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'building_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'door_house_no': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'floor_no': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'routes': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),


            # 'sales_staff': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
          
        }



class DefaultBottleQuantityForm(forms.ModelForm):
    def __init__(self,branch, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
    class Meta:
        model = Customers
        fields = ['customer_name','no_of_bottles_required']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'no_of_bottles_required': forms.TextInput(attrs={'class': 'form-control', 'required': 'true','type':'number'}),
            # 'sales_staff': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
          
        }

class CustodyPullOutForm(forms.ModelForm):
    def __init__(self,customer_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['request_type'].queryset = RequestTypeMaster.objects.filter(request_name__in = ['Custody Pull Out'])
        customer_items = Customer_Custody_Items.objects.filter(customer=customer_id).values_list('product', flat=True)
        self.fields['item_name'].queryset = Product.objects.filter(product_id__in=customer_items)
        #self.fields['qty_to_be_taken_out'].queryset = Customer_Custody_Items.objects.filter(customer = customer_id).count

    class Meta:
        model = CustodyPullOutModel
        fields = ['request_type','item_name','qty_to_be_taken_out','scheduled_date','customer_custody_item']
        widgets = {
            'request_type': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'item_name': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'qty_to_be_taken_out': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'scheduled_date':forms.DateInput(attrs={'class': 'form-control','type':'date', 'required': 'true'}),
            'customer_custody_item': forms.TextInput(attrs={'class': 'form-control','type':'hidden', 'required': 'true'}),
        }

class DiffBottles_Create_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['request_type'].queryset = RequestTypeMaster.objects.exclude(request_name__in = ['Coupons','Others'])
        self.fields['mode'].choices = [
            (choice[0], choice[1]) for choice in self.fields['mode'].choices]
    class Meta:
        model = DiffBottlesModel
        fields = ['quantity_required','delivery_date','assign_this_to','mode','amount','request_type']

        widgets = {
            'quantity_required': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'delivery_date': forms.DateInput(attrs={'class': 'form-control', 'type':'date','required': True}),
            'assign_this_to': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
            'mode': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'amount': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'request_type': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),

        }



class Other_Req_Create_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['request_type'].queryset = RequestTypeMaster.objects.exclude(request_name__in = ['Coupons','Dispenser','Empty Bottles','Filled Bottles'])

        
    class Meta:
        model = OtherRequirementModel
        fields = ['requirement','request_type']

        widgets = {
            'requirement': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'request_type': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),

           
        }

class Coupon_Create_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['request_type'].queryset = RequestTypeMaster.objects.exclude(request_name__in = ['Custody Pull Out','Others'])
        self.fields['coupon_type'].choices = [
            (choice[0], choice[1]) for choice in self.fields['coupon_type'].choices]
        self.fields['category'].choices = [
            (choice[0], choice[1]) for choice in self.fields['category'].choices]
        self.fields['payment_status'].choices = [
            (choice[0], choice[1]) for choice in self.fields['payment_status'].choices]
    class Meta:
        model = CouponPurchaseModel
        fields = ['coupon_type','category','number_of_books','payment_status','amount','free_coupon','discount','delivery_date','request_type']

        widgets = {
            'coupon_type': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'category': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'number_of_books': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'payment_status': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'amount': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'free_coupon': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'discount': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'delivery_date': forms.DateInput(attrs={'class': 'form-control', 'type':'date','required': True}),
            'request_type': forms.Select(attrs={'class': 'form-control', 'required': 'true'}),

        }
      