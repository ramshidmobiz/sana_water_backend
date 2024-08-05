from django import forms
from django.forms import ModelForm
from .models import *
from accounts.models import *
from master.models import *

class VanForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['driver'].queryset = CustomUser.objects.filter(user_type='Driver')
        self.fields['salesman'].queryset = CustomUser.objects.filter(user_type='Salesman')

    class Meta:
        model = Van
        fields = ['van_make', 'plate', 'renewal_date', 'insurance_expiry_date', 'capacity', 'branch_id','salesman','driver','bottle_count']

        widgets = {
            'van_make' : forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'plate' : forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'renewal_date': forms.DateInput(attrs={'class': 'form-control', 'type':'date','required': 'true'}),
            'insurance_expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type':'date','required': 'true'}),
            'capacity' : forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'driver' : forms.Select(attrs={"class": "form-control", 'required': 'true'}),
            'salesman' : forms.Select(attrs={"class": "form-control", 'required': 'true'}),
            'bottle_count' : forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
        }


class EditVanForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['driver'].queryset = CustomUser.objects.filter(user_type='Driver')
        self.fields['salesman'].queryset = CustomUser.objects.filter(user_type='Salesman')

    class Meta:
        model = Van
        fields = ['van_make', 'plate', 'renewal_date', 'insurance_expiry_date', 'capacity', 'branch_id','salesman','driver','bottle_count']

        widgets = {
            'van_make' : forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'plate' : forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'renewal_date': forms.DateInput(attrs={'class': 'form-control', 'type':'date','required': 'true'}),
            'insurance_expiry_date': forms.DateInput(attrs={'class': 'form-control','type':'date', 'required': 'true'}),
            'capacity' : forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'driver' : forms.Select(attrs={"class": "form-control", 'required': 'true'}),
            'salesman' : forms.Select(attrs={"class": "form-control", 'required': 'true'}),
            'bottle_count' : forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
        }


class VanAssociationForm(forms.Form):
    van = forms.ModelChoiceField(queryset=Van.objects.all(), label='Select Van',        widget=forms.Select(attrs={'class': 'form-control', 'required': 'true'})
)
    driver = forms.ModelChoiceField(queryset=CustomUser.objects.filter(user_type='Driver'), label='Select Driver' ,widget=forms.Select(attrs={'class': 'form-control', 'required': 'true'})
)
    salesman = forms.ModelChoiceField(queryset=CustomUser.objects.filter(user_type='Salesman'),        widget=forms.Select(attrs={'class': 'form-control', 'required': 'true'})
)

class EditAssignForm(forms.ModelForm):
    class Meta:
        model = Van
        fields = ['driver', 'salesman']

    def __init__(self, *args, **kwargs):
        super(EditAssignForm, self).__init__(*args, **kwargs)
        self.fields['driver'].queryset = CustomUser.objects.filter(user_type='driver')
        self.fields['salesman'].queryset = CustomUser.objects.filter(user_type='salesman')





class VanAssignRoutesForm(forms.ModelForm):
    class Meta:
        model = Van_Routes
        fields = [ 'routes']

        widgets = {
            'routes' : forms.Select(attrs={"class": "form-control", 'required': 'true'}),
        }

# Licence 
class Licence_Add_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    class Meta:
        model = Van_License
        fields = ['van', 'emirate','license_no','expiry_date']
        widgets = {
            'van': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'emirate': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'license_no': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control','type':'date', 'required': 'true'}),
        }


class Licence_Edit_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['emirate'].queryset = EmirateMaster.objects.filter()
    class Meta:
        model = Van_License
        fields = ['emirate','expiry_date','license_no']
        widgets = {
            
            'emirate': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control','type':'date', 'required': 'true'}),
            'license_no': forms.TextInput(attrs={'class': 'form-control', 'required': True}),

        }




# Expense
class ExpenseHeadForm(forms.ModelForm):
    class Meta:
        model = ExpenseHead
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ExpenseAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['route'].queryset = RouteMaster.objects.all()
        self.fields['van'].queryset = Van.objects.all()
    class Meta:
        model = Expense
        fields = ['expence_type', 'route', 'van', 'amount', 'expense_date', 'remarks']
        widgets = {
            'expence_type': forms.Select(attrs={'class': 'form-control'}),
            'route': forms.Select(attrs={'class': 'form-control', 'required':True}),
            'van': forms.Select(attrs={'class': 'form-control', 'required':True}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'expense_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
    
class ExpenseEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['route'].queryset = RouteMaster.objects.all()
        self.fields['van'].queryset = Van.objects.all()
    class Meta:
        model = Expense
        fields = ['route', 'van', 'amount', 'expense_date', 'remarks']
        widgets = {
            'route': forms.Select(attrs={'class': 'form-control', 'required':True}),
            'van': forms.Select(attrs={'class': 'form-control', 'required':True}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'expense_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        
        
class BottleAllocationForm(forms.ModelForm):
    class Meta:
        model = BottleAllocation
        fields = ['route', 'fivegallon_count', 'reason']
        widgets = {
            'route': forms.Select(attrs={'class': 'form-control'}),
            'fivegallon_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        } 

class ExcessBottleCountForm(forms.ModelForm):
    class Meta:
        model = ExcessBottleCount
        fields = ['van', 'bottle_count', 'route']
        