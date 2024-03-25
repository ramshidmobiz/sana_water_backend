import uuid
import json
import base64
import datetime

from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect,HttpResponse,get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView

from competitor_analysis.forms import CompetitorAnalysisFilterForm
from master.functions import generate_form_errors
from .forms import *
from .models import *
from django.db.models import Q


# Create your views here.
def user_login(request):
    template_name = 'registration/user_login.html'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = CustomUser.objects.get(username = username)
        user = authenticate(username=username, password=password)
        # print("::::::::::::::::::::::::::",user)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('dashboard')
            else:
                context = {'error_msg': 'Invalid Username or Password'}
                return render(request, template_name, context)
        else:
            context = {'error_msg': 'User Doest Not exist'}
            return render(request, template_name, context)
        
    return render(request, template_name)   

class UserLogout(View):

    def get(self, request):
        try:
            logout(request)
            messages.success(request, 'Successfully logged out', extra_tags='success')
            return redirect("login")
        except Exception as e:
            # Handle exceptions if necessary
            messages.error(request, 'An error occurred while logging out', extra_tags='danger')
            return redirect("login")
        
class Users_List(View):
    template_name = 'accounts/user_list.html'

    def get(self, request, *args, **kwargs):
        user_li = CustomUser.objects.filter()
        context = {'user_li': user_li}
        return render(request, self.template_name, context)

class User_Create(View):
    template_name = 'accounts/user_create.html'
    form_class = User_Create_Form

    def get(self, request, *args, **kwargs):
        context = {'form': self.form_class}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            passw = make_password(data.password)
            data.password = passw
            data.save()
            messages.success(request, 'User Successfully Added.', 'alert-success')
            return redirect('users')
        else:
            #print(form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Field: {field}, Error: {error}")
            messages.success(request, 'Data is not valid.', 'alert-danger')
            context = {'form': form}
            return render(request, self.template_name, context)


class User_Edit(View):
    template_name = 'accounts/user_edit.html'
    form_class = User_Edit_Form

    def get(self, request, pk, *args, **kwargs):
        rec = CustomUser.objects.get(id=pk)
        form = self.form_class(instance=rec)
        context = {'form': form,'rec':rec}
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        rec = CustomUser.objects.get(id=pk)
        form = self.form_class(request.POST, request.FILES, instance=rec)
        if form.is_valid():
            data = form.save(commit=False)
            #data.modified_by = request.user
            data.modified_date = datetime.now()
            data.save()
            messages.success(request, 'User Data Successfully Updated', 'alert-success')
            return redirect('users')
        else:
            #print(form.errors)
            messages.success(request, 'Data is not valid.', 'alert-danger')
            context = {'form': form}
            return render(request, self.template_name, context)

class User_Details(View):
    template_name = 'accounts/user_details.html'

    def get(self, request, pk, *args, **kwargs):
        user_det = CustomUser.objects.get(id=pk)
        context = {'user_det': user_det}
        return render(request, self.template_name, context)  
    

# class Customer_List(View):
#     template_name = 'accounts/customer_list.html'

#     def get(self, request, *args, **kwargs):
#         # Create an instance of the form and populate it with GET data
#         form = CompetitorAnalysisFilterForm(request.GET)
        
#         user_li = Customers.objects.all()
#         query = request.GET.get("q")
#         if query:
#             user_li = user_li.filter(
#                 Q(customer_name__icontains=query) |
#                 Q(mobile_no__icontains=query) |
#                 Q(routes__route_name__icontains=query) |
#                 Q(location__location_name__icontains=query)|
#                 Q(building_name__icontains=query)
#             )

#         # Check if the form is valid
#         # if form.is_valid():
#             # Filter the queryset based on the form data
#         route_filter = request.GET.get('route_name')
#         if route_filter :
#             user_li = Customers.objects.filter(routes__route_name=route_filter)
#         # else:
#         #         user_li = Customers.objects.all()
#         # else:
#         #     # If the form is not valid, retrieve all customers
#         #     user_li = Customers.objects.all()
#         route_li = RouteMaster.objects.all()
#         context = {'user_li': user_li, 'form': form, 'route_li': route_li}
#         return render(request, self.template_name, context)

class Customer_List(View):
    template_name = 'accounts/customer_list.html'

    def get(self, request, *args, **kwargs):
        # Retrieve the query parameter
        query = request.GET.get("q")
        route_filter = request.GET.get('route_name')
        # Start with all customers
        user_li = Customers.objects.all()

        # Apply filters if they exist
        if query:
            user_li = user_li.filter(
                Q(customer_name__icontains=query) |
                Q(mobile_no__icontains=query) |
                Q(routes__route_name__icontains=query) |
                Q(location__location_name__icontains=query) |
                Q(building_name__icontains=query)
            )

        if route_filter:
            user_li = user_li.filter(routes__route_name=route_filter)

        # Get all route names for the dropdown
        route_li = RouteMaster.objects.all()

        context = {'user_li': user_li, 'route_li': route_li}
        return render(request, self.template_name, context)
    

def create_customer(request):
    branch = request.user.branch_id
    form = CustomercreateForm(branch)
    template_name = 'accounts/create_customer.html'
    context = {"form":form}
    try:
        if request.method == 'POST':
            form = CustomercreateForm(branch,data = request.POST)
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
                return redirect('customers')
            else:
                messages.success(request, 'Invalid form data. Please check the input.')
                return render(request, template_name,context)
        return render(request, template_name,context)
    except Exception as e:
            print(":::::::::::::::::::::::",e)
            messages.success(request, 'Something went wrong')
            return render(request, template_name,context)

class Customer_Details(View):
    template_name = 'accounts/customer_details.html'

    def get(self, request, pk, *args, **kwargs):
        user_det = Customers.objects.get(customer_id=pk)
        context = {'user_det': user_det}
        return render(request, self.template_name, context) 
    

def edit_customer(request,pk):
    branch = request.user.branch_id
    cust_Data = Customers.objects.get(customer_id = pk)
    form = CustomerEditForm(branch,instance = cust_Data)
    template_name = 'accounts/edit_customer.html'
    context = {"form":form}
    try:
        if request.method == 'POST':
            form = CustomerEditForm(branch,instance = cust_Data,data = request.POST)
            context = {"form":form}
            if form.is_valid():
                data = form.save(commit=False)
                data.emirate = data.location.emirate
                data.save()
                messages.success(request, 'Customer Details Updated successfully!')
                return redirect('customers')
            else:
                messages.success(request, 'Invalid form data. Please check the input.')
                return render(request, template_name,context)
        return render(request, template_name,context)
    except Exception as e:
        print(":::::::::::::::::::::::",e)
        messages.success(request, 'Something went wrong')
        return render(request, template_name,context)

# def visit_days_assign(request,customer_id):
#     template_name = 'accounts/assign_dayof_visit.html'
#     customer_data=Customers.objects.get(customer_id = customer_id)
#     day_visits = Staff_Day_of_Visit.objects.get(customer_id__customer_id = customer_id)
#     form = Day_OfVisit_Form(instance=day_visits)
#     context = {'day_visits' : day_visits,"form":form,"customer_data":customer_data}
#     if request.method == 'POST':
#         context = {'day_visits' : day_visits,"form":form,"customer_data":customer_data}
#         form = Day_OfVisit_Form(request.POST,instance=day_visits)
#         if form.is_valid():
#             data = form.save(commit=False)
#             data.created_by = str(request.user)
#             data.created_date = datetime.now()
#             data.save()
#             messages.success(request, 'Day of visit updated successfully!')
#             return redirect('customers')
#         else:
#             messages.success(request, 'Invalid form data. Please check the input.')
#             return render(request, template_name,context)
#     return render(request,template_name ,context)


def visit_days_assign(request, customer_id):
    template_name = 'accounts/assign_dayof_visit.html'
    
    try:
        customer_data = Customers.objects.get(customer_id=customer_id)
    except Customers.DoesNotExist:
        messages.error(request, 'Customer does not exist.')
        return redirect('customers')
    
    form = Day_OfVisit_Form()
    message_content = "Day of visit updated successfully!"

    day_visits = None
    if Staff_Day_of_Visit.objects.filter(customer_id=customer_data).exists():
        day_visits = Staff_Day_of_Visit.objects.get(customer_id=customer_data)
        form = Day_OfVisit_Form(instance=day_visits)
        message_content = "Day of visit created successfully!"
        
    if request.method == 'POST':
        form = Day_OfVisit_Form(request.POST, instance=day_visits)
        if form.is_valid():
            data = form.save(commit=False)
            data.created_by = str(request.user)
            data.created_date = datetime.now()
            data.save()
            messages.success(request, message_content)
            return redirect('customers')
        else:
            messages.error(request, 'Invalid form data. Please check the input.')
    
    context = {
        "form": form,
        'day_visits': day_visits,
        "customer_data": customer_data
    }
    
    return render(request, template_name, context)

