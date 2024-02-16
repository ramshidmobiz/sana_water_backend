import json
import string
import random
import openpyxl
import datetime

from django.views import View
from django.urls import reverse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.db import transaction, IntegrityError
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from master.functions import generate_form_errors
from competitor_analysis.forms import CompetitorAnalysisFilterForm


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
    

class Customer_List(View):
    template_name = 'accounts/customer_list.html'

    def get(self, request, *args, **kwargs):
        # Create an instance of the form and populate it with GET data
        form = CompetitorAnalysisFilterForm(request.GET)

        # Check if the form is valid
        if form.is_valid():
            # Filter the queryset based on the form data
            route_filter = form.cleaned_data.get('route_name')
            if route_filter :
                user_li = Customers.objects.filter(routes__route_name=route_filter)
            else:
                user_li = Customers.objects.all()
        else:
            # If the form is not valid, retrieve all customers
            user_li = Customers.objects.all()

        context = {'user_li': user_li, 'form': form}
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

# @login_required
# @role_required(['superadmin'])
def generate_customer_id(length=6):
    """Generate a random customer ID."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def upload_customer(request):
    if request.method == 'POST':
        form = CustomerFileForm(request.POST,request.FILES) 
        
        if form.is_valid():
            input_excel = request.FILES['file']
            try:
                book = openpyxl.load_workbook(input_excel)
                sheet = book.active  # Assuming the first sheet is the one you want to read
                dict_list = []

                for row in sheet.iter_rows(min_row=2, values_only=True):  # Start from the second row (assuming headers are in the first row)
                    data = {
                        'customer_name': row[0],
                        'building_name': row[1],
                        'door_house_no': row[2],
                        'floor_no': row[3],
                        'mobile_no': row[4],
                        'whats_app': row[5],
                        'email_id': row[6],
                        'customer_type': row[7],
                        'sales_type': row[8],
                        'no_of_bottles_required': row[9],
                        'emirates': row[10],
                        'branch': row[11],
                        'location': row[12],
                        'route': row[13],
                        'price': row[14],
                    }
                    dict_list.append(data)

                    with transaction.atomic():
                        for item in dict_list:
                            name = item['customer_name']
                            building_name = item['building_name']
                            door_house_no = item['door_house_no']
                            floor_no = item['floor_no']
                            mobile_no = item['mobile_no']
                            whats_app = item['whats_app']
                            email_id = item['email_id']
                            customer_type = item['customer_type']
                            sales_type = item['sales_type']
                            no_of_bottles_required = item['no_of_bottles_required']
                            emirate = item['emirates']
                            branch = item['branch']
                            location = item['location']
                            route = item['route']
                            price = item['price']
                            
                            if not Customers.objects.filter(customer_name=name,door_house_no=door_house_no).exists():
                            
                                # Fetch or create BranchMaster
                                branch_instance = BranchMaster.objects.filter(name=branch).first() or \
                                                    BranchMaster.objects.create(
                                                        created_by=request.user.username,
                                                        created_date=datetime.now(),
                                                        name=branch,
                                                    )
                                
                                # Fetch or create EmirateMaster
                                emirate_instance = EmirateMaster.objects.filter(name=emirate).first() or \
                                                    EmirateMaster.objects.create(
                                                        created_by=request.user.username,
                                                        created_date=datetime.now(),
                                                        name=emirate,
                                                    )
                                
                                # Fetch or create RouteMaster
                                route_instance = RouteMaster.objects.filter(route_name=route).first() or \
                                                    RouteMaster.objects.create(
                                                        created_by=request.user.username,
                                                        created_date=datetime.now(),
                                                        route_name=route,
                                                        branch_id=branch_instance,
                                                    )
                                
                                # Fetch or create LocationMaster
                                location_instance = LocationMaster.objects.filter(location_name=location).first() or \
                                                    LocationMaster.objects.create(
                                                        created_by=request.user.username,
                                                        created_date=datetime.now(),
                                                        location_name=location,
                                                        emirate=emirate_instance,
                                                        branch_id=branch_instance,
                                                    )
                                
                                # Create User
                                user_data = CustomUser.objects.create_user(
                                    username=name,
                                    password="test123",
                                    is_active=True,
                                )
                                
                                # Add user to 'customer' group
                                group = Group.objects.get_or_create(name="customer")[0]
                                user_data.groups.add(group)
                                
                                # Generate customer ID
                                customer_id = generate_customer_id()
                                
                                # Create Customer
                                customer = Customers.objects.create(
                                    customer_id=customer_id,
                                    customer_name=name,
                                    building_name=building_name,
                                    door_house_no=door_house_no,
                                    floor_no=floor_no,
                                    routes=route_instance,
                                    location=location_instance,
                                    emirate=emirate_instance,
                                    mobile_no=mobile_no,
                                    whats_app=whats_app,
                                    email_id=email_id,
                                    customer_type=customer_type,
                                    sales_type=sales_type,
                                    no_of_bottles_required=no_of_bottles_required,
                                    rate=price,
                                    branch_id=branch_instance,
                                )
                                customer.save()

                                response_data = {
                                    "status" : "true",
                                    "title" : "Successfully Uploaded",
                                    "message" : "Customer Successfully Added.",
                                    "redirect" : "true",
                                    "redirect_url" : reverse('customers')
                                }    
                            
            except IntegrityError as e:
                response_data = {
                    "status": "false",
                    "title": "Failed",
                    "message": str(e),
                }

            except Exception as e:
                response_data = {
                    "status": "false",
                    "title": "Failed",
                    "message": str(e),
                }               
        else:
            form = CustomerFileForm()
            message =generate_form_errors(form , formset=False)
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = CustomerFileForm()

        context = {
            "form" : form,
            'page_name' : 'Upload customers',
            'page_title' : 'Upload Location',
            "redirect" : True,
            "is_need_popup_box" : True,
            "is_need_dropzone" : True,
            "is_upload" : True,
        }
        return render(request, 'accounts/import_customer.html',context)