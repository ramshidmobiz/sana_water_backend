from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import  *
from accounts.models import *
from master.models import *
from product.models import *

import json
from django.core.serializers import serialize
from django.views import View
from datetime import datetime
from client_management.models import Customer_Custody_Items
from master.forms import *
# Create your views here.
from accounts.models import Customers
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404


class RequestType_List(View):
    template_name = 'customer_care/requesttype_list.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        category_li = RequestTypeMaster.objects.all()
        context = {'category_li': category_li}
        return render(request, self.template_name, context)

class RequestType_Create(View):
    template_name = 'customer_care/requesttype_create.html'
    form_class = RequestType_Create_Form

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
            messages.success(request, 'Category Successfully Added.', 'alert-success')
            return redirect('requesttype_list')
        else:
            #print(form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Field: {field}, Error: {error}")
            messages.success(request, 'Data is not valid.', 'alert-danger')
            context = {'form': form}
            return render(request, self.template_name, context)

class RequestType_Edit(View):
    template_name = 'customer_care/requesttype_edit.html'
    form_class = RequestType_Edit_Form

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        rec = RequestTypeMaster.objects.get(request_id=pk)
        form = self.form_class(instance=rec)
        context = {'form': form,'rec':rec}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, pk, *args, **kwargs):
        rec = RequestTypeMaster.objects.get(request_id=pk)
        form = self.form_class(request.POST, request.FILES, instance=rec)
        if form.is_valid():
            data = form.save(commit=False)
            data.modified_by = str(request.user.id)
            data.modified_date = datetime.now()
            data.save()
            messages.success(request, 'Category Data Successfully Updated', 'alert-success')
            return redirect('requesttype_list')
        else:
            #print(form.errors)
            messages.success(request, 'Data is not valid.', 'alert-danger')
            context = {'form': form}
            return render(request, self.template_name, context)

class RequestType_Details(View):
    template_name = 'customer_care/requesttype_details.html'

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        category_det = RequestTypeMaster.objects.get(request_id=pk)
        context = {'category_det': category_det}
        return render(request, self.template_name, context)



def createcustomer(request):
    branch = request.user.branch_id
    form = CustomercreateForms(branch)
    template_name = 'accounts/create_customer.html'
    context = {"form":form}
    try:
        if request.method == 'POST':
            form = CustomercreateForms(branch,data = request.POST)
            context = {"form":form}
            if form.is_valid():
                data = form.save(commit=False)
                data.created_by = str(request.user)
                data.created_date = datetime.now()
                data.emirate = data.location.emirate
                branch_id=request.user.branch_id.branch_id
                branch = BranchMaster.objects.get(branch_id=branch_id)  # Adjust the criteria based on your model
                data.branch_id = branch
                data.save()
                Staff_Day_of_Visit.objects.create(customer = data)
                messages.success(request, 'Customer Created successfully!')
                return redirect('requestType')
            else:
                messages.success(request, 'Invalid form data. Please check the input.')
                return render(request, template_name,context)
        return render(request, template_name,context)
    except Exception as e:
            print(":::::::::::::::::::::::",e)
            messages.success(request, 'Something went wrong')
            return render(request, template_name,context)

def requestType(request):
    all_requestType = Customers.objects.all()
    print("hdfhjfasH",all_requestType)
    context = {'all_requestType': all_requestType}
    return render(request, 'customer_care/all_customers.html', context)


         

def change_of_address(request,pk):
    branch = request.user.branch_id
    cust_Data = Customers.objects.get(pk = pk)
    form = ChangeofaddressForm(branch,instance = cust_Data)
    template_name = 'customer_care/changeofaddress.html'
    context = {"form":form}
    try:
        if request.method == 'POST':
            form = ChangeofaddressForm(branch,instance = cust_Data,data = request.POST)
            context = {"form":form}
            if form.is_valid():
                data = form.save(commit=False)
                data.save()
                messages.success(request, 'Customer Details Updated successfully!')
                return redirect('requestType')
            else:
                messages.success(request, 'Invalid form data. Please check the input.')
                return render(request, template_name,context)
        return render(request, template_name,context)
    except Exception as e:
        print(":::::::::::::::::::::::",e)
        messages.success(request, 'Something went wrong')
        return render(request, template_name,context)                      
   

def default_bottle_qty(request,pk):
    branch = request.user.branch_id
    cust_Data = Customers.objects.get(pk = pk)
    form = DefaultBottleQuantityForm(branch,instance = cust_Data)
    template_name = 'customer_care/default_bottleqty.html'
    context = {"form":form}
    try:
        if request.method == 'POST':
            form = DefaultBottleQuantityForm(branch,instance = cust_Data,data = request.POST)
            context = {"form":form}
            if form.is_valid():
                data = form.save(commit=False)
                data.save()
                messages.success(request, 'Default bottle qty Updated successfully!')
                return redirect('requestType')
            else:
                messages.success(request, 'Invalid form data. Please check the input.')
                return render(request, template_name,context)
        return render(request, template_name,context)
    except Exception as e:
        print(":::::::::::::::::::::::",e)
        messages.success(request, 'Something went wrong')
        return render(request, template_name,context)                   
   
def get_item_quantity(request):
    if request.method == "GET":
        try:
            customer = request.GET['customer']
            item_name = request.GET['item_name']
            item_count = Customer_Custody_Items.objects.get(customer=customer,product=item_name)
            dat = {'item_count': item_count.count,'customer_custody_item':item_count.custody_item_id}
            return JsonResponse(dat)
        except:
            dat = {'item_count': ''}
            return JsonResponse(dat)
   
def custody_pullout(request, pk):
    cust_data = Customers.objects.get(pk=pk)
    count = Customer_Custody_Items.objects.get(customer=cust_data).count
    item_name = Customer_Custody_Items.objects.get(customer=cust_data).product

    template_name = 'customer_care/custodypullout.html'
    context = {"count": count, "item_name": item_name, "cust_data": cust_data}

    try:
        if request.method == 'POST':
            item_name = request.POST.get('name')
            print("item_name", item_name)
            scheduled_date = request.POST.get('Scheduleddate')
            count = request.POST.get('count')
            print("count", count)

            form = CustodyPullOutForm(request.POST)

            if form.is_valid():
                data = form.save(commit=False)
                data.save()
                messages.success(request, 'Default bottle qty Updated successfully!')
                return redirect('requestType')
            else:
                messages.error(request, 'Invalid form data. Please check the input.')
                context["form"] = form
                return render(request, template_name, context)

        # GET request
        form = CustodyPullOutForm(
            initial={'item_name': item_name, 'qty_to_be_taken_out': count, 'scheduled_date': scheduled_date}
        )
        context["form"] = form

        return render(request, template_name, context)

    except Exception as e:
        print(":::::::::::::::::::::::", e)
        messages.error(request, 'Something went wrong')
        return render(request, template_name, context)
    
class Bottle_List(ListAPIView):
    template_name = 'customer_care/bottle_list.html'

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        id_customer = Customers.objects.get(pk=pk).customer_id
        bottle_list_exists = DiffBottlesModel.objects.filter(customer=pk).exists()
        bottle_list=[]
        if bottle_list_exists:
            bottle_list = DiffBottlesModel.objects.filter(customer=pk)
            print('bottle_list',bottle_list)
        context = {'bottle_list': bottle_list,'customer_id':id_customer}
        return render(request,'customer_care/bottle_list.html',context)

    

class Diffbottles_Create(View):
    template_name = 'customer_care/bottle_create.html'
    form_class = DiffBottles_Create_Form

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        try:
            id_customer = Customers.objects.get(pk=pk).customer_id
            context = {'form': self.form_class}
            return render(request, self.template_name, context)
        except Exception as e:
            print(e)
            return render(request, self.template_name, context)
        

    def post(self, request, pk, *args, **kwargs):
        try:
            print(request.POST,"====")
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                data = form.save(commit=False)
                id_customer = Customers.objects.get(pk=pk)
                data.customer = id_customer
                data.created_by = str(request.user.id)
                data.save()
                messages.success(request, 'Bottles Successfully Added.', 'alert-success')
                return redirect('requestType')
            else:
            #print(form.errors)
                for field, errors in form.errors.items():
                    for error in errors:
                        print(f"Field: {field}, Error: {error}")
                messages.success(request, 'Data is not valid.', 'alert-danger')
                context = {'form': form}
                return render(request, self.template_name, context)
        except Exception as e:
            print(e)
            return render(request,'customer_care/bottle_create.html')
        


class Other_List(ListAPIView):
    template_name = 'customer_care/other_list.html'

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        id_customer = Customers.objects.get(pk=pk).customer_id
        other_list_exists = OtherRequirementModel.objects.filter(customer=pk).exists()
        other_list=[]
        if other_list_exists:
            other_list = OtherRequirementModel.objects.filter(customer=pk)
            print('other_list',other_list)
        context = {'other_list': other_list,'customer_id':id_customer}
        return render(request,'customer_care/other_list.html',context)
        
class Other_Req_Create(View):
    template_name = 'customer_care/otherrequirement_create.html'
    form_class = Other_Req_Create_Form
    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):        
        try:
            id_customer = Customers.objects.get(pk=pk).customer_id
            #requestype_obj = RequestTypeMaster.objects.exclude(request_name__in = ['Coupons','Others'])
            #print("requestype_obj=====",requestype_obj)
            context = {'form': self.form_class}            
            return render(request, self.template_name, context)
        except Exception as e:
            print(e)
            return render(request, self.template_name, context)
        
    def post(self, request, pk, *args, **kwargs):
        try:
            print(request.POST,"====")
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                data = form.save(commit=False)
                id_customer = Customers.objects.get(pk=pk)
                data.customer = id_customer
                data.created_by = str(request.user.id)
                data.save()
                messages.success(request, 'requirement Successfully Added.', 'alert-success')
                return redirect('requestType')
            else:
            #print(form.errors)
                for field, errors in form.errors.items():
                    for error in errors:
                        print(f"Field: {field}, Error: {error}")
                messages.success(request, 'Data is not valid.', 'alert-danger')
                context = {'form': form}
                return render(request, self.template_name, context)
        except Exception as e:
            print(e)
            return render(request,'customer_care/otherrequirement_create.html')
        
class Custody_Pullout_List(ListAPIView):
    template_name = 'customer_care/custody_pullout_list.html'

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        id_customer = Customers.objects.get(pk=pk).customer_id
        custody_pullout_list=[]
        custody_customer_exists = Customer_Custody_Items.objects.filter(customer=id_customer).exists()
        if custody_customer_exists:
            # count = Customer_Custody_Items.objects.get(customer=id_customer).count
            # print('count',count)
            # item_name = Customer_Custody_Items.objects.get(customer=id_customer).product
            # print("item_name",item_name)
            custody_pullout_list_exists = CustodyPullOutModel.objects.filter(customer=pk).exists()
            if custody_pullout_list_exists:
                custody_pullout_list = CustodyPullOutModel.objects.filter(customer=pk)
                print('custody_pullout_list',custody_pullout_list)
        context = {'custody_pullout_list': custody_pullout_list,'customer_id':id_customer}
        return render(request,'customer_care/custody_pullout_list.html',context)



        
class Custody_Pullout_Create(View):
    template_name = 'customer_care/custody_pullout_create.html'
    form_class = CustodyPullOutForm

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):        
        try:
            id_customer = Customers.objects.get(pk=pk).customer_id
            #requestype_obj = RequestTypeMaster.objects.exclude(request_name__in = ['Coupons','Others'])
            #print("requestype_obj=====",requestype_obj)
            form_instance = self.form_class(id_customer)

            context = {'form': form_instance,'customer':id_customer} 
            print(context,"contex")           
            return render(request, self.template_name, context)
        except Exception as e:
            print(e)
            return render(request, self.template_name, context)
        
    def post(self, request, pk, *args, **kwargs):
        try:
            print(request.POST,"====request.POST")
            form = self.form_class(pk,request.POST)
            if form.is_valid():
                print("inside form")
                data = form.save(commit=False)
                id_customer = Customers.objects.get(pk=pk)
                print(id_customer,"<-----id_customer")
                data.customer = id_customer
                data.created_by = str(request.user.id)
                data.save()
                print(data,"====data")
                messages.success(request, 'Custody Pullout Successfully Added.', 'alert-success')
                return redirect('custody_pullout_list',pk)
            else:
                print(form.errors)
                for field, errors in form.errors.items():
                    for error in errors:
                        print(f"Field: {field}, Error: {error}")
                messages.success(request, 'Data is not valid.', 'alert-danger')
                context = {'form': form}
                return render(request, self.template_name, context)
        except Exception as e:
            print("error",e)
            return render(request,'customer_care/custody_pullout_create.html')
        
class Coupon_Purchse_List(ListAPIView):
    template_name = 'customer_care/coupon_list.html' 

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        id_customer = Customers.objects.get(pk=pk).customer_id
        coupon_list_exists = CouponPurchaseModel.objects.filter(customer=pk).exists()
        coupon_list=[]
        if coupon_list_exists:
            coupon_list = CouponPurchaseModel.objects.filter(customer=pk)
            print('coupon_list',coupon_list)
        context = {'coupon_list': coupon_list,'customer_id':id_customer}
        return render(request,'customer_care/coupon_list.html',context)

class Coupon_Purchse_Create(View):
    template_name = 'customer_care/coupon_create.html'
    form_class = Coupon_Create_Form


    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        try:
            id_customer = Customers.objects.get(pk=pk).customer_id
            context = {'form': self.form_class}
            return render(request, self.template_name, context)
        except Exception as e:
            print(e)
            return render(request, self.template_name, context)
        

    def post(self, request, pk, *args, **kwargs):
        try:
            print(request.POST,"====")
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                data = form.save(commit=False)
                id_customer = Customers.objects.get(pk=pk)
                data.customer = id_customer
                data.created_by = str(request.user.id)
                data.save()
                messages.success(request, 'Coupon purchased Successfully .', 'alert-success')
                return redirect('requestType')
            else:
            #print(form.errors)
                for field, errors in form.errors.items():
                    for error in errors:
                        print(f"Field: {field}, Error: {error}")
                messages.success(request, 'Data is not valid.', 'alert-danger')
                context = {'form': form}
                return render(request, self.template_name, context)
        except Exception as e:
            print(e)
            return render(request,'customer_care/coupon_create.html')