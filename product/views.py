from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import datetime
from django.contrib import messages
from django.shortcuts import render, redirect,HttpResponse
from django.views import View
from .forms import *
import uuid
from accounts.models import *
from .models import *
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from coupon_management.models import *
from van_management.models import *

from django.shortcuts import redirect, get_object_or_404


class Products_List(View):
    template_name = 'products/products_list.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        product_li = Product.objects.filter()
        context = {'product_li': product_li}
        return render(request, self.template_name, context)

class Product_Create(View):
    template_name = 'products/product_create.html'
    form_class = Products_Create_Form

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = {'form': self.form_class}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = {'form': self.form_class}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        

        if form.is_valid():
            category_id = form.data.get('category_id')
            product_name = form.data.get('product_name')
            print("category_id",category_id)
            get_category = CategoryMaster.objects.get(category_id=category_id)
            data = form.save(commit=False)
            data.created_by = str(request.user.id)
            branch_id=request.user.branch_id.branch_id
            branch = BranchMaster.objects.get(branch_id=branch_id)  # Adjust the criteria based on your model
            data.branch_id = branch
            if get_category.category_name =='Coupons':
                save_in_coupon_type = CouponType.objects.create(coupon_type_name = product_name,
                                        no_of_leaflets =0,
                                        valuable_leaflets =0,
                                        free_leaflets =0 ,
                                        created_by =str(request.user.id))
                
            data.save()

            messages.success(request, 'Product Successfully Added.', 'alert-success')
            return redirect('products')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Field: {field}, Error: {error}")
           

            messages.success(request, 'Data is not valid.', 'alert-danger')
            context = {'form': form}
            return render(request, self.template_name, context)


class Product_Edit(View):
    template_name = 'products/product_edit.html'
    form_class = Products_Edit_Form

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        rec = Product.objects.get(product_id=pk)
        form = self.form_class(instance=rec)
        context = {'form': form,'rec':rec}
        return render(request, self.template_name, context)
 
    @method_decorator(login_required)
    def post(self, request, pk, *args, **kwargs):
        rec = Product.objects.get(product_id=pk)
        form = self.form_class(request.POST, request.FILES, instance=rec)
        if form.is_valid():
            data = form.save(commit=False)
            print(request)
            data.modified_by = str(request.user.id)
            data.modified_date = datetime.now()
            data.save()
            messages.success(request, 'Product Data Successfully Updated', 'alert-success')
            return redirect('products')
        else:
            #print(form.errors)
            messages.success(request, 'Data is not valid.', 'alert-danger')
            context = {'form': form}
            return render(request, self.template_name, context)

class Product_Details(View):
    template_name = 'products/product_details.html'

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        product_det = Product.objects.get(product_id=pk)
        context = {'product_det': product_det}
        return render(request, self.template_name, context)   

class ProductDelete(View):
    template_name = 'products/product_delete_confirm.html'  # Template for deletion confirmation

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, product_id=pk)
        context = {'product_det': product}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, product_id=pk)
        product.delete()
        return redirect('products')  # Redirect to product list after deletion 

class Defaultprice_List(View):
    template_name = 'products/defaultprice.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        def_price_list = Product_Default_Price_Level.objects.filter()
        context = {'def_price_list': def_price_list}
        return render(request, self.template_name, context)
    

class Defaultprice_Create(View):
    template_name = 'products/defaultprice_create.html'
    form_class = Defaultprice_Create_Form

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        
        context = {'form': self.form_class}
        return render(request, self.template_name, context)
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form  = self.form_class(request.POST)
        if form.is_valid():
            default_price = form.save(commit=False)
            default_price.created_by = str(request.user.id)
            default_price.save()
            messages.success(request, 'Set Default Price Successfully ', 'alert-success')
            return redirect('defaultprice')
        else:
            context = {'form':form}
            return render(request, self.template_name, context)



class Defaultprice_Edit(View):
    template_name = 'products/defaultprice_edit.html'
    form_class = Defaultprice_Edit_Form

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        rec = Product_Default_Price_Level.objects.get(def_price_id=pk)
        form = self.form_class(instance=rec)
        context = {'form': form,'rec':rec,'product':rec.product_id}
        return render(request, self.template_name, context) 
    
    @method_decorator(login_required)
    def post(self, request, pk, *args, **kwargs):
        rec = Product_Default_Price_Level.objects.get(def_price_id=pk)
        form = self.form_class(request.POST, request.FILES, instance=rec)
        if form.is_valid():
            data = form.save(commit=False)
            data.modified_by = str(request.user.id)
            data.modified_date = datetime.now()
            data.save()
            messages.success(request, 'Default Price Successfully Updated', 'alert-success')
            return redirect('defaultprice')
        else:
            #print(form.errors)
            messages.success(request, 'Data is not valid.', 'alert-danger')
            context = {'form': form}
            return render(request, self.template_name, context)


class Defaultprice_Delete(View):
    def get(self, request, product_name, *args, **kwargs):
        
        return render(request, 'products/defaultprice_delete.html', {'product':product_name})
    def post(self, requset, product_name, *args, **kwargs):
        product = Product.objects.get(product_name = product_name)
        default_prices = Product_Default_Price_Level.objects.filter(product_id = product)
        print(default_prices)
        for default_price in default_prices:
            default_price.delete()
        
        print(default_prices)
        return redirect('defaultprice')

#------------------Issue Orders------------------------------------

        
def staffIssueOrdersList(request):
    staff_orders_details = Staff_Orders_details.objects.all()

    context = {'staff_orders_details': staff_orders_details}
    return render(request, 'products/staff_issue_orders_list.html', context)

def staffIssueOrdersCreate(request,staff_order_details_id):

    issue = get_object_or_404(Staff_Orders_details, staff_order_details_id=staff_order_details_id)
    print("issue",issue)
    
    count = issue.count
    print("count",count)
    product_id =issue.product_id
    print("product_id",product_id)
    product_category= issue.product_id.category_id
    print("product_category",product_category)
    productunit=issue.product_id.unit
    print("productunit",productunit)
    staff_Orders_details_id=issue.staff_order_details_id
    staff_order_id=issue.staff_order_id
    print("staff_order_id",staff_order_id)
    order_number=issue.staff_order_id.order_number
    if request.method == 'POST':
        form = StaffIssueOrdersForm(request.POST)
        # print("form",form)
        if form.is_valid():
            # Get the AssignStaffCoupon instance from the form
            print("VALID")
            data = form.save(commit=False)
            # Calculate stock quantity
            quantity_issued = int(form.data.get('quantity_issued'))
            stock_quantity =   quantity_issued - int(count)

            
            
            # Set other fields such as created_by, modified_by, etc.
            
            data.created_by = str(request.user.id)
            data.modified_by = str(request.user.id)
            data.modified_date = datetime.now()
            data.created_date = datetime.now()
            data.product_id=product_id
            data.staff_Orders_details_id=issue
            data.stock_quantity= stock_quantity
            # Set other fields as needed...

            # Save the instance
            data.save()

            return redirect('staff_issue_orders_list')  # Redirect to a success page or another URL
    else:
        form = StaffIssueOrdersForm()
    

    
    
    return render(request, 'products/staff_issue_orders_create.html', {
        'count': count,
        'product_id':product_id,
        'product_category':product_category,
        'productunit':productunit,
        'order_number':order_number,
        'form':form,
        
    })
