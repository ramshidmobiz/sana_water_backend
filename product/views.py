import json
import datetime

from django.views import View
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render,redirect,reverse
from django.db import transaction, IntegrityError
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from coupon_management.serializers import couponStockSerializers
from master.functions import generate_form_errors
from .forms import *
import uuid
from accounts.models import *
from .models import *
from coupon_management.models import *
from van_management.models import *

from django.template.loader import get_template
import pandas as pd
from xhtml2pdf import pisa

def get_coupon_bookno(request):
    request_id = request.GET.get("request_id")
    print(request_id, "request_id")
    
    if (instances := Staff_Orders_details.objects.filter(pk=request_id)).exists():
        instance = instances.first()
        stock_instances = CouponStock.objects.filter(couponbook__coupon_type__coupon_type_name=instance.product_id.product_name,coupon_stock="company")
        serialized = couponStockSerializers(stock_instances, many=True)
        # print(serialized.data)
        status_code = 200
        response_data = {
            "status": "true",
            "data": serialized.data,
        }
    else:
        status_code = 404
        response_data = {
            "status": "false",
            "title": "Failed",
            "message": "item not found",
        }

    return HttpResponse(json.dumps(response_data),status=status_code, content_type="application/json")

def get_product_items(request):
    category_id = request.GET.get("category_id")
    product_items = ProdutItemMaster.objects.filter(category__pk=category_id)
    data = [{'id': item.id, 'name': item.product_name} for item in product_items]

    return JsonResponse(data, safe=False)
    
class Product_items_List(View):
    template_name = 'products/product_items_list.html'
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        product_items = ProdutItemMaster.objects.filter()
        context = {'product_items': product_items}
        return render(request, self.template_name, context)
    
class Product_items_Create(View):
    template_name = 'products/product_items_create.html'
    form_class = Product_Item_Create_Form

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = {'form': self.form_class}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.created_by = str(request.user.id)
            data.save()
            
            if data.category.category_name == 'Coupons':
                product_name = data.product_name
                if not CouponType.objects.filter(coupon_type_name=product_name).exists():
                    CouponType.objects.create(
                        coupon_type_name=product_name,
                        no_of_leaflets=0,
                        valuable_leaflets=0,
                        free_leaflets=0,
                        created_by=str(request.user.id)
                    )
            messages.success(request, 'Product Item Successfully Added.', 'alert-success')
            return redirect('product_items')
        else:
            #print(form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Field: {field}, Error: {error}")
            messages.success(request, 'Data is not valid.', 'alert-danger')
            context = {'form': form}
            return render(request, self.template_name, context)


class Product_Item_Edit(View):
    template_name = 'products/product_items_create.html'
    form_class = Product_Item_Create_Form

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        rec = ProdutItemMaster.objects.get(id=pk)
        form = self.form_class(instance=rec)
        context = {'form': form,'rec':rec}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, pk, *args, **kwargs):
        rec = ProdutItemMaster.objects.get(id=pk)
        pre_name = rec.product_name
        form = self.form_class(request.POST, request.FILES, instance=rec)
        if form.is_valid():
            data = form.save(commit=False)
            data.modified_by = str(request.user.id)
            data.modified_date = datetime.now()
            data.save()
            
            if rec.category.category_name == 'Coupons':
                if (instances:=CouponType.objects.filter(coupon_type_name=pre_name)).exists():
                    instances.update(coupon_type_name=data.product_name)
            
            messages.success(request, 'Product Item Data Successfully Updated', 'alert-success')
            return redirect('product_items')
        else:
            #print(form.errors)
            messages.success(request, 'Data is not valid.', 'alert-danger')
            context = {'form': form}
            return render(request, self.template_name, context)   

# @method_decorator(login_required)    
def delete_product_item(request, pk):
    """
    delete product_item,
    :param request:
    :param pk:
    :return:
    """
    instance = ProdutItemMaster.objects.get(pk=pk)
    if instance.category.category_name == 'Coupons':
        if (instances:=CouponType.objects.filter(coupon_type_name=instance.product_name)).exists():
                    instances.delete()
    instance.delete()
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Product Item Successfully Deleted.",
        "reload": "true",
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')
          
class Products_List(View):
    template_name = 'products/products_list.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        instances = Product.objects.all().order_by('-created_date')
        context = {'instances': instances}
        return render(request, self.template_name, context)

class Product_Create(View):
    template_name = 'products/product_create.html'
    form_class = Products_Create_Form
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        # product_items = ProdutItemMaster.objects.all()  # Fetch all product items
        context = {'form': form, }
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        
        if form.is_valid():
            product_item = ProdutItemMaster.objects.get(pk=form.data.get('product_name'))
            
            data = Product(
                product_name=product_item,
                created_by = str(request.user.id),
                branch_id=request.user.branch_id,
                quantity=form.data.get('quantity')
            )
            data.save()
            
            if request.user.branch_id:
                try:
                    branch_id = request.user.branch_id.branch_id
                    branch = BranchMaster.objects.get(branch_id=branch_id)  
                    data.branch_id = branch
                    
                    if (stock_intances:=ProductStock.objects.filter(product_name=data.product_name,branch=data.branch_id)).exists():
                        stock_intance = stock_intances.first()
                        stock_intance.quantity += int(data.quantity)
                        stock_intance.save()
                    else:
                        ProductStock.objects.create(
                            product_name=data.product_name,
                            branch=data.branch_id,
                            quantity=int(data.quantity)
                        )
                        
                except ObjectDoesNotExist:
                    # Handle the case where branch_id is not found
                    messages.error(request, 'Branch information not found for the current user.')


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
    form_class = Products_Create_Form

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

# def staff_issue_orders_list(request):
#     instances = Staff_Orders.objects.all().order_by('-created_date')
    
#     filter_data = {}
#     query = request.GET.get("q")
    
#     if query:

#         instances = instances.filter(
#             Q(order_number__icontains=query)
#         )
#         title = "Staff issue Orders - %s" % query
#         filter_data['q'] = query

#     context = {'instances': instances}
#     return render(request, 'products/staff_issue_orders_list.html', context)
    

def staff_issue_orders_list(request):
    instances = Staff_Orders.objects.filter().order_by('-created_date')
    
    filter_data = {}
    query = request.GET.get("q")
    date_param = request.GET.get("date")

    if query:
        instances = instances.filter(
            Q(order_number__icontains=query)
        )
        title = "Staff issue Orders - %s" % query
        filter_data['q'] = query
        
    if date_param:
        date = datetime.strptime(date_param, "%Y-%m-%d").date()
        instances = instances.filter(order_date=date)
        filter_data['date'] = date_param
    else:
        instances = instances.filter(order_date=timezone.now().date())

    context = {
        'instances': instances,
        'filter_data': filter_data
        }
    return render(request, 'products/staff_issue_orders_list.html', context)
        
def staff_issue_orders_details_list(request,staff_order_id):
    order = Staff_Orders.objects.get(pk=staff_order_id)
    staff_orders_details = Staff_Orders_details.objects.filter(staff_order_id=order)
    
    context = {
        'staff_orders_details': staff_orders_details.order_by('-created_date'),
        'order_date': order.order_date,
        'order_number': order.order_number
        }
    return render(request, 'products/staff_issue_orders_details_list.html', context)

@transaction.atomic
def staffIssueOrdersCreate(request, staff_order_details_id):
    issue = get_object_or_404(Staff_Orders_details, staff_order_details_id=staff_order_details_id)
    van = Van.objects.get(salesman_id__id=issue.staff_order_id.created_by)
    try:
        vanstock = VanProductStock.objects.get(created_date=issue.staff_order_id.order_date,van=van,product__product_name="5 Gallon")
        vanstock_count = vanstock.stock
    except :
        vanstock_count = 0
    
    if request.method == 'POST':
        form = StaffIssueOrdersForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    product_stock = ProductStock.objects.get(product_name=issue.product_id)
                    stock_quantity = issue.count
                    
                    quantity_issued = form.cleaned_data.get('quantity_issued')
                    
                    if issue.product_id.product_name == "5 Gallon":
                        if int(quantity_issued) != 0 and van.bottle_count > int(quantity_issued) + vanstock_count:
                            van_limit=True
                        else:
                            van_limit=False
                    else:
                        van_limit = True
                        
                    if van_limit:
                        if 0 < int(quantity_issued) <= int(product_stock.quantity):
                            # Creating Staff Issue Order
                            data = form.save(commit=False)
                            # data.created_by = request.user.id
                            data.modified_by = request.user.id
                            data.modified_date = datetime.now()
                            data.created_date = datetime.now()
                            data.product_id = issue.product_id
                            data.staff_Orders_details_id = issue
                            data.stock_quantity = stock_quantity
                            data.quantity_issued = int(data.quantity_issued) + int(quantity_issued)
                            data.van = van
                            data.save()
                            
                            # Updating ProductStock
                            product_stock.quantity -= int(quantity_issued)
                            product_stock.save()
                            
                            # Updating VanStock and VanProductStock
                            # van = Van.objects.get(salesman_id__id=form.cleaned_data.get('salesman_id').pk)
                            vanstock = VanStock.objects.create(
                                created_by=request.user.id,
                                created_date=datetime.now(),
                                modified_by=request.user.id,
                                modified_date=datetime.now(),
                                van=van,
                                stock_type='opening_stock',
                            )
                            VanProductItems.objects.create(
                                product=issue.product_id,
                                count=int(quantity_issued),
                                van_stock=vanstock,
                            )
                            
                            if VanProductStock.objects.filter(created_date=datetime.today().date(),product=issue.product_id,van=van).exists():
                                van_product_stock = VanProductStock.objects.get(created_date=datetime.today().date(),product=issue.product_id,van=van)
                                van_product_stock.stock += int(quantity_issued)
                                van_product_stock.save()
                            else:
                                van_product_stock = VanProductStock.objects.create(
                                    created_date=datetime.now().date(),
                                    product=issue.product_id,
                                    van=van,
                                    stock=int(quantity_issued)
                                    )
                                
                            if issue.product_id.product_name == "5 Gallon":
                                if (bottle_count:=BottleCount.objects.filter(
                                    van=van_product_stock.van,
                                    created_date__date=van_product_stock.created_date
                                    )).exists():
                                    
                                    bottle_count = bottle_count.first()
                                else:
                                    bottle_count = BottleCount.objects.create(van=van_product_stock.van,created_date=van_product_stock.created_date)
                                bottle_count.opening_stock += van_product_stock.stock
                                bottle_count.save()
                            
                            issue.issued_qty += int(quantity_issued)
                            issue.save()
                            
                            response_data = {
                                "status": "true",
                                "title": "Successfully Created",
                                "message": "created successfully.",
                                'redirect': 'true',
                                "redirect_url": reverse('staff_issue_orders_list')
                            }
                        else:
                            response_data = {
                                "status": "false",
                                "title": "Failed",
                                "message": f"No stock available in {product_stock.product_name}, only {product_stock.quantity} left",
                            }
                    else:
                        response_data = {
                            "status": "false",
                            "title": "Failed",
                            "message": f"Over Load! currently {vanstock_count} Can Loaded, Max 5 Gallon Limit is {van.bottle_count}",
                        }
                        
            except IntegrityError as e:
                # Handle database integrity error
                response_data = {
                    "status": "false",
                    "title": "Failed",
                    "message": str(e),
                }

            except Exception as e:
                # Handle other exceptions
                response_data = {
                    "status": "false",
                    "title": "Failed",
                    "message": str(e),
                }
        else:
            message = generate_form_errors(form, formset=False)
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = StaffIssueOrdersForm()
    
        context = {
            'form': form,
            'issue_instance': issue,
            'max_van_bottle_count': van.bottle_count,
            'van_current_stock_bottle_count': vanstock_count,
        }
        return render(request, 'products/coupon_issue_orders_create.html', context)

# def issue_coupons_orders(request):
#     staff_order_details_id = request.GET.get("request_id")
#     issue_instance = get_object_or_404(Staff_Orders_details, staff_order_details_id=staff_order_details_id)
    
#     if request.method == 'POST':
#         form = StaffIssue_CouponsOrdersForm(request.POST)
                
#         if form.is_valid():
#             try:
#                 with transaction.atomic():
#                     update_purchase_stock = ProductStock.objects.filter(product_name=issue_instance.product_id)

#                     if update_purchase_stock.exists():  # Check if any records are returned
#                         ptoduct_stockQuantity = update_purchase_stock.first().quantity
#                         if ptoduct_stockQuantity is None:
#                             ptoduct_stockQuantity = 0
#                     else:
#                         ptoduct_stockQuantity = 0  # Default value if no records are found

#                     quantity_issued = form.cleaned_data.get('quantity_issued')

#                     if 0 < int(quantity_issued) <= ptoduct_stockQuantity:
#                         coupon = NewCoupon.objects.get(coupon_type__coupon_type_name=issue_instance.product_id.product_name,book_num=coupon_no)
                        
#                         data = form.save(commit=False)
#                         data.created_by = str(request.user.id)
#                         data.modified_by = str(request.user.id)
#                         data.modified_date = datetime.now()
#                         data.created_date = datetime.now()
#                         data.product_id = issue_instance.product_id
#                         data.staff_Orders_details_id = issue_instance
#                         data.coupon_book = coupon
#                         data.save()
                        
#                         #  ProductStock
#                         update_purchase_stock = update_purchase_stock.first()
#                         update_purchase_stock.quantity -= int(data.quantity_issued)
#                         update_purchase_stock.save()
                        
#                         # Update VanStock
#                         van = Van.objects.get(salesman_id__id=issue_instance.staff_order_id.created_by)
                        
#                         if (update_van_stock:=VanCouponStock.objects.filter(van=van,coupon=coupon,stock_type="opening_stock")).exists():
#                             van_stock = update_van_stock.first()
#                             van_stock.count += int(data.quantity_issued)
#                             van_stock.save()
#                         else:
#                             vanstock = VanStock.objects.create(
#                                 created_by=str(request.user.id),
#                                 created_date=datetime.now(),
#                                 van=van,
#                                 stock_type="opening_stock",
#                             )
                            
#                             VanCouponItems.objects.create(
#                                 coupon=coupon,
#                                 book_no=coupon_no,
#                                 coupon_type=coupon.coupon_type,
#                                 van_stock=vanstock,
#                             )
                            
#                             van_stock = VanCouponStock.objects.create(
#                                 coupon=coupon,
#                                 stock_type="opening_stock",
#                                 count=int(data.quantity_issued),
#                                 van=van
#                             )
                            
#                         issue_count_balance = int(issue_instance.count) - int(data.quantity_issued)
                        
#                         issue_instance.count = issue_count_balance
#                         issue_instance.save()
                        
#                         CouponStock.objects.filter(couponbook=coupon).update(coupon_stock="van")
                        
#                         response_data = {
#                             "status": "true",
#                             "title": "Successfully Created",
#                             "message": "Coupon Isued successfully.",
#                             'redirect': 'true',
#                             "redirect_url": reverse('staff_issue_orders_list')
#                         }
#                     else:
#                         response_data = {
#                             "status": "false",
#                             "title": "Failed",
#                             "message": f"No stock available in {issue_instance.product_id.product_name}, only {ptoduct_stockQuantity} left",
#                         }
            
#             except IntegrityError as e:
#                 # Handle database integrity error
#                 response_data = {
#                     "status": "false",
#                     "title": "Failed",
#                     "message": str(e),
#                 }

#             except Exception as e:
#                 # Handle other exceptions
#                 response_data = {
#                     "status": "false",
#                     "title": "Failed",
#                     "message": str(e),
#                 }
#         else:
#             message = generate_form_errors(form,formset=False)
            
#             response_data = {
#                 "status": "false",
#                 "title": "Failed",
#                 "message": message,
#             }
#         return HttpResponse(json.dumps(response_data), content_type='application/javascript')
#     else:
#         form = StaffIssue_CouponsOrdersForm(initial={"coupo_no":coupon_no})
        
#     context = {
#         'form': form,
#         'issue_instance':issue_instance,
#     }
#     return render(request, 'products/coupon_issue_orders_create.html', context)


# def issue_coupons_orders(request, staff_order_details_id):
#     coupon_no = request.GET.get("coupo_no")
#     print("coupon_no",coupon_no)
#     issue = get_object_or_404(Staff_Orders_details, staff_order_details_id=staff_order_details_id)
#     count = issue.count
#     product_id = issue.product_id
#     print("product_id",product_id)
#     productunit = issue.product_id.unit
#     product_category = issue.product_id.category_id.category_name

#     if product_category == 'Coupons':
#         print("Product is present")

#         product = issue.product_id 
#         if product:
#             product_name = product.product_name
#             print("Product Name:", product_name)

#             coupontypes = CouponType.objects.filter(coupon_type_name=product_name)
#             print("coupontypes", coupontypes)

           
#             if coupontypes.exists():
                
#                 for coupontype in coupontypes:
#                     print("Coupon Type:", coupontype.coupon_type_name)
#                     coupontype_id = coupontype.coupon_type_id
#                     print("coupontype_id",coupontype_id)
#                     couponbook = NewCoupon.objects.filter(coupon_type__coupon_type_id=coupontype_id)
#                     print("couponbook",couponbook)
#                     if request.method == 'POST':
#                         form = StaffIssue_CouponsOrdersForm(request.POST)
#                         if form.is_valid():
#                             data = form.save(commit=False)
#                             quantity_issued = int(form.cleaned_data.get('quantity_issued'))
#                             print("quantity_issued",quantity_issued)
                            

#                             #  ProductStock 
#                             product_stock = ProductStock.objects.get(product=product)
#                             product_stock.quantity = int(form.cleaned_data.get('quantity_issued'))
#                             product_stock.save()
                                            
                         
#                             # Update VanStock
#                             salesman_id = form.cleaned_data.get('salesman_id')
#                             salesman = CustomUser.objects.get(id=salesman_id.id)
#                             van = Van.objects.get(salesman_id=salesman)  
#                             print("van",van)
                            
#                             van_stock = VanStock.objects.create(
#                                 created_by=str(request.user.id),
#                                 modified_by=str(request.user.id),
#                                 van=van )
#                             print("van_stock",van_stock)
                            
#                              # Set other fields
#                             data.created_by = str(request.user.id)
#                             data.modified_by = str(request.user.id)
#                             data.modified_date = datetime.now()
#                             data.created_date = datetime.now()
#                             data.product_id = product_id
#                             data.staff_Orders_details_id = issue
#                             data.stock_quantity = stock_quantity

#                             data.save()
#                             return redirect('staff_issue_orders_list')
#                         else:
#                             print(form.errors)

#                     form = StaffIssue_CouponsOrdersForm(initial={"coupo_no":coupon_no})
#                     return render(request,'products/coupon_issue_orders_create.html',{'form': form,
#                                                                                       'product_name':product_name,
#                                                                                       'productunit':productunit,
#                                                                                       'product_category': product_category,
#                                                                                       'count': count,'product_id': product_id,})

#             else:
#                 print("No CouponType found for the product name")

#         else:
#             print("Product not found or product_id is None")

#     return render(request, 'products/staff_issue_orders_list.html')


# def issue_coupons_orders(request, staff_order_details_id):
#     issue = get_object_or_404(Staff_Orders_details, staff_order_details_id=staff_order_details_id)
#     count = issue.count
#     product_id = issue.product_id.product_id
#     productunit = issue.product_id.unit
#     product_category = issue.product_id.category_id.category_name

#     if product_category == 'Coupons':
#         print("Product is present")

#         product = issue.product_id 
#         if product:
#             product_name = product.product_name
#             print("Product Name:", product_name)

#             coupontypes = CouponType.objects.filter(coupon_type_name=product_name)
#             print("coupontypes", coupontypes)

           
#             if coupontypes.exists():
                
#                 for coupontype in coupontypes:
#                     print("Coupon Type:", coupontype.coupon_type_name)
#                     coupontype_id = coupontype.coupon_type_id
#                     print("coupontype_id",coupontype_id)
#                     couponbook = NewCoupon.objects.filter(coupon_type__coupon_type_id=coupontype_id)
#                     print("couponbook",couponbook)
#                     if request.method == 'POST':
#                         form = StaffIssueOrdersForm(request.POST)
#                         if form.is_valid():
#                             data = form.save(commit=False)
#                             quantity_issued = int(form.cleaned_data.get('quantity_issued'))
#                             stock_quantity = issue.product_id.quantity - quantity_issued  # Subtract issued quantity from stock

#                             # Update the product's stock quantity
#                             product.quantity = stock_quantity
#                             product.save()

#                             # Update ProductStock
#                             product_stock, _ = ProductStock.objects.get_or_create(product=product)
#                             product_stock.quantity = stock_quantity
#                             product_stock.save()
                            
#                             # Update VanStock
#                             salesman_id = form.cleaned_data.get('salesman_id')
#                             salesman = CustomUser.objects.get(id=salesman_id.id)
#                             van = Van.objects.get(salesman_id=salesman)  
#                             print("van",van)
#                             van_stock, _ = VanStock.objects.get_or_create(van=van, defaults={
#                                 'created_by': str(request.user.id),
#                                 'modified_by': str(request.user.id),
#                             })

#                             # Update VanCouponItems or VanProductItems based on product category
#                             if product_category == "Coupons":
#                                 van_coupon_item, _ = VanCouponItems.objects.get_or_create(coupon=product.coupon_book, van_stock=van_stock)
#                                 van_coupon_item.book_no = product.coupon_book.book_no
#                                 van_coupon_item.coupon_type = product.coupon_book.coupon_type
#                                 van_coupon_item.save()

#                                 van_coupon_stock, _ = VanCouponStock.objects.get_or_create(coupon=product.coupon_book)
#                                 van_coupon_stock.count += quantity_issued
#                                 van_coupon_stock.save()
#                             else:
#                                 van_product_item, _ = VanProductItems.objects.get_or_create(product=product, van_stock=van_stock)
#                                 van_product_item.count += quantity_issued
#                                 van_product_item.save()

#                                 van_product_stock, _ = VanProductStock.objects.get_or_create(product=product)
#                                 van_product_stock.count += quantity_issued
#                                 van_product_stock.save()
                            
#                             # Set other fields and save the form
#                             data.created_by = str(request.user.id)
#                             data.modified_by = str(request.user.id)
#                             data.modified_date = timezone.now()
#                             data.created_date = timezone.now()
#                             data.product_id = product_id
#                             data.staff_Orders_details_id = issue
#                             data.stock_quantity = stock_quantity
#                             data.save()

#                             return redirect('staff_issue_orders_list')

#                     form = StaffIssue_CouponsOrdersForm()
#                     return render(request,'products/coupon_issue_orders_create.html',{'form': form,'couponbook':couponbook,
#                                                                                       'product_name':product_name,
#                                                                                       'productunit':productunit,
#                                                                                       'product_category': product_category,
#                                                                                       'count': count,'product_id': product_id,})

#             else:
#                 print("No CouponType found for the product name")

#         else:
#             print("Product not found or product_id is None")

#     return render(request, 'products/staff_issue_orders_list.html')

from django.http import JsonResponse

def issue_coupons_orders(request):
    if request.method == 'POST':
        request_id = request.POST.get("request_id")
        book_numbers = request.POST.getlist("coupon_book_no")
        
        issue = get_object_or_404(Staff_Orders_details, staff_order_details_id=request_id)
        
        for book_no in book_numbers :
            coupon = NewCoupon.objects.get(book_num=book_no,coupon_type__coupon_type_name=issue.product_id.product_name)
            update_purchase_stock = ProductStock.objects.filter(product_name=issue.product_id)
            
            if update_purchase_stock.exists():  
                ptoduct_stockQuantity = update_purchase_stock.first().quantity
                if ptoduct_stockQuantity is None:
                    ptoduct_stockQuantity = 0
            else:
                ptoduct_stockQuantity = 0
                quantity_issued = issue.issued_qty
            
            # if int(issue.issued_qty) > 0 and ptoduct_stockQuantity >= int(issue.issued_qty):
            try:
                with transaction.atomic():
                    issue_order = Staff_IssueOrders.objects.create(
                        created_by = str(request.user.id),
                        modified_by = str(request.user.id),
                        modified_date = datetime.now(),
                        # created_date = datetime.now(),
                        product_id = issue.product_id,
                        staff_Orders_details_id = issue,
                        coupon_book = coupon,
                        quantity_issued = 1
                    )
                    
                    #  ProductStock
                    update_purchase_stock = update_purchase_stock.first()
                    update_purchase_stock.quantity -= 1
                    update_purchase_stock.save()
                    
                    # Update VanStock
                    van = Van.objects.get(salesman_id__id=issue.staff_order_id.created_by)
                    
                    if (update_van_stock:=VanCouponStock.objects.filter(created_date=datetime.today().date(),van=van,coupon=coupon)).exists():
                        van_stock = update_van_stock.first()
                        van_stock.stock += 1
                        van_stock.save()
                    else:
                        vanstock = VanStock.objects.create(
                            created_by=str(request.user.id),
                            created_date=datetime.now(),
                            van=van,
                            stock_type="opening_stock",
                        )
                        
                        VanCouponItems.objects.create(
                            coupon=coupon,
                            book_no=coupon,
                            coupon_type=coupon.coupon_type,
                            van_stock=vanstock,
                        )
                        
                        van_stock = VanCouponStock.objects.create(
                            created_date=datetime.now().date(),
                            coupon=coupon,
                            stock=1,
                            van=van
                        )
                        
                        issue.issued_qty += 1
                        issue.save()
                            
                        CouponStock.objects.filter(couponbook=coupon).update(coupon_stock="van")
                        
                        response_data = {
                            "status": "true",
                            "title": "Successfully Created",
                            "message": "Coupon Isued successfully.",
                            'redirect': 'true',
                            "redirect_url": reverse('staff_issue_orders_list')
                        }
                        
            except IntegrityError as e:
                # Handle database integrity error
                response_data = {
                    "status": "false",
                    "title": "Failed",
                    "message": str(e),
                }

            except Exception as e:
                # Handle other exceptions
                response_data = {
                    "status": "false",
                    "title": "Failed",
                    "message": str(e),
                }
            # else:
            #     response_data = {
            #         "status": "false",
            #         "title": "Failed",
            #         "message": f"No stock available in {issue.product_id.product_name}, only {ptoduct_stockQuantity} left",
            #     }
                
        return JsonResponse(response_data)


#---------------------REPORTS-----
def product_stock_report(request):
    instances = ProductStock.objects.order_by('-created_date')  # Order by latest created date

    return render(request, 'products/product_report.html', {'instances': instances})

def download_productstock_pdf(request):
    instances = ProductStock.objects.order_by('-created_date')  # Order by latest created date
    template_path = 'products/product_stock_pdf_template.html'
    context = {'instances': instances}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="product_stock_details.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    # Create PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def product_stock_excel_download(request):
    # Retrieve product stock data
    product_stocks = ProductStock.objects.order_by('-created_date')  # Order by latest created date


    # Create a dictionary to store data
    data = {
        
        'Product Name': [product_stock.product_name for product_stock in product_stocks],
        'Stock Quantity': [product_stock.quantity for product_stock in product_stocks],
        'Branch': [product_stock.branch for product_stock in product_stocks],
        'Status': [product_stock.status for product_stock in product_stocks],
        
    }

    # Create a DataFrame from the data dictionary
    df = pd.DataFrame(data)

    # Create a buffer to store the Excel file
    buffer = BytesIO()

    # Write the DataFrame to the buffer in Excel format
    df.to_excel(buffer, index=False)

    # Set the buffer's file pointer to the beginning
    buffer.seek(0)

    # Create the HttpResponse object with the Excel file
    filename = f"product_stock_{timezone.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response


@login_required
def stock_transfer_view(request):
    bottle_count = WashingStock.objects.get(product__product_name="5 Gallon").quantity
    if request.method == "POST":
        form = StockTransferForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product_id']
            used_quantity = form.cleaned_data['used_quantity']
            damage_quantity = form.cleaned_data['damage_quantity']
            
            try:
                with transaction.atomic():
                    product_item = ProdutItemMaster.objects.get(pk=product_id.pk)

                    if used_quantity and used_quantity > 0:
                        WashedProductTransfer.objects.create(
                            product=product_item,
                            quantity=used_quantity,
                            status="used",
                            created_by=request.user,
                            created_date=timezone.now(),
                        )

                        used_product, created = WashedUsedProduct.objects.get_or_create(product=product_item)
                        used_product.quantity += used_quantity
                        used_product.save()

                        washing_stock = WashingStock.objects.get(product=product_item)
                        washing_stock.quantity -= used_quantity
                        washing_stock.save()

                    if damage_quantity and damage_quantity > 0:
                        WashedProductTransfer.objects.create(
                            product=product_item,
                            quantity=damage_quantity,
                            status="scrap",
                            created_by=request.user,
                            created_date=timezone.now(),
                        )

                        ScrapProductStock.objects.create(
                            product=product_item,
                            quantity=damage_quantity,
                            created_by=request.user,
                            created_date=timezone.now(),
                        )

                        scrap_product, created = ScrapStock.objects.get_or_create(product=product_item)
                        scrap_product.quantity += damage_quantity
                        scrap_product.save()

                        washing_stock = WashingStock.objects.get(product=product_item)
                        washing_stock.quantity -= damage_quantity
                        washing_stock.save()

                    return redirect('dashboard')  
            except IntegrityError as e:
                form.add_error(None, str(e))
            except Exception as e:
                form.add_error(None, str(e))

    else:
        form = StockTransferForm()

    return render(request, 'products/stock_transfer.html', {'form': form,'bottle_count':bottle_count})


@login_required
def scrap_stock_transfer_view(request):
    scrap_stocks = ScrapStock.objects.filter(product__product_name="5 Gallon").aggregate(total_quantity=Sum('quantity'))['total_quantity']

    if request.method == "POST":
        form = ScrapStockForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            cleared_quantity = form.cleaned_data['cleared_quantity']
            
            try:
                with transaction.atomic():
                    ScrapcleanedStock.objects.create(
                        product=product,
                        quantity=cleared_quantity,
                        created_by=request.user.username,
                        created_date=timezone.now(),
                    )

                    scrap_stock = ScrapStock.objects.get(product=product)
                    scrap_stock.quantity -= cleared_quantity
                    scrap_stock.save()

                    return redirect('scrap_stock_transfer_view')

            except IntegrityError as e:
                form.add_error(None, str(e))
            except Exception as e:
                form.add_error(None, str(e))

    else:
        form = ScrapStockForm()

    return render(request, 'products/scrap_stock_transfer.html', {'form': form, 'scrap_stocks': scrap_stocks})