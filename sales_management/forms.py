# forms.py
from django import forms
from django.db.models import Q
from master.models import RouteMaster  # Assuming you have imported RouteMaster
from accounts.models import Customers

class SaleEntryFilterForm(forms.Form):
    route_name = forms.ModelChoiceField(
        queryset=RouteMaster.objects.all(),
        empty_label="All Routes",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'required': 'true'})
    )

    search_query = forms.CharField(
        label='Search',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


from django import forms
from product.models import Product
from master.models import CategoryMaster


class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=CategoryMaster.objects.all(),
        label='Category',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    product_name = forms.ModelChoiceField(
        queryset=Product.objects.none(), 
        label='Product',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    coupon_method = forms.BooleanField(
        label='Select Coupon', 
        required=False, 
        widget=forms.RadioSelect(choices=[('digital', 'Digital'), ('manual', 'Manual')])
    )

    class Meta:
        model = Product
        fields = ['category', 'product_name', 'coupon_method']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['product_name'].queryset = Product.objects.filter(category_id=category_id).order_by('product_name')
            except (ValueError, TypeError):
                pass
        elif self.instance.category_id is not None:
            self.fields['product_name'].queryset = self.instance.category_id.product_set.order_by('product_name')
        else:
            self.fields['product_name'].queryset = Product.objects.none()

        # Set default value for coupon_method
        self.fields['coupon_method'].initial = 'manual'



from django import forms
from .models import SalesExtraModel



class CashCustomerSaleForm(forms.ModelForm):
    status = forms.ChoiceField(choices=SalesExtraModel.STATUS_CHOICES, widget=forms.Select)

    def __init__(self, *args, **kwargs):
        super(CashCustomerSaleForm, self).__init__(*args, **kwargs)
        # Add form-control class to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            # Set required attribute to False for all fields
            field.required = False

        # Prepopulate bottle_variations field
        empty_bottles = self.instance.empty_bottles if self.instance else None
        collected_bottles = self.instance.collected_bottles if self.instance else None
        self.fields['bottle_variations'].initial = max(0, empty_bottles - collected_bottles) if empty_bottles is not None and collected_bottles is not None else 0

    class Meta:
        model = SalesExtraModel
        fields = ['qty_needed', 'empty_bottles', 'collected_bottles', 'bottle_variations']


class CreditCustomerSaleForm(forms.ModelForm):
    status = forms.ChoiceField(choices=SalesExtraModel.STATUS_CHOICES, widget=forms.Select)

    def __init__(self, *args, **kwargs):
        super(CreditCustomerSaleForm, self).__init__(*args, **kwargs)
        # Add form-control class to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        # Prepopulate bottle_variations field
        empty_bottles = self.instance.empty_bottles if self.instance else None
        collected_bottles = self.instance.collected_bottles if self.instance else None
        self.fields['bottle_variations'].initial = max(0, empty_bottles - collected_bottles) if empty_bottles is not None and collected_bottles is not None else 0

    class Meta:
        model = SalesExtraModel
        fields = ['qty_needed', 'empty_bottles', 'collected_bottles', 'bottle_variations']

class CashCouponCustomerSaleForm(forms.ModelForm):
    status = forms.ChoiceField(choices=SalesExtraModel.STATUS_CHOICES, widget=forms.Select)

    def __init__(self, *args, **kwargs):
        super(CashCouponCustomerSaleForm, self).__init__(*args, **kwargs)
        # Add form-control class to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        # Prepopulate bottle_variations field
        empty_bottles = self.instance.empty_bottles if self.instance else None
        collected_bottles = self.instance.collected_bottles if self.instance else None
        self.fields['bottle_variations'].initial = max(0, empty_bottles - collected_bottles) if empty_bottles is not None and collected_bottles is not None else 0

    class Meta:
        model = SalesExtraModel
        fields = ['qty_needed', 'no_of_coupons', 'empty_bottles', 'collected_bottles', 'bottle_variations']

class CreditCouponCustomerSaleForm(forms.ModelForm):
    status = forms.ChoiceField(choices=SalesExtraModel.STATUS_CHOICES, widget=forms.Select)

    def __init__(self, *args, **kwargs):
        super(CreditCouponCustomerSaleForm, self).__init__(*args, **kwargs)
        # Add form-control class to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        # Prepopulate bottle_variations field
        empty_bottles = self.instance.empty_bottles if self.instance else None
        collected_bottles = self.instance.collected_bottles if self.instance else None
        self.fields['bottle_variations'].initial = max(0, empty_bottles - collected_bottles) if empty_bottles is not None and collected_bottles is not None else 0

    class Meta:
        model = SalesExtraModel
        fields = ['qty_needed', 'no_of_coupons', 'coupon_variations', 'empty_bottles', 'collected_bottles', 'bottle_variations']

