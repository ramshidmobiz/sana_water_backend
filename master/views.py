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
from django.contrib.auth.hashers import make_password, check_password
from .models import *


from . serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication 
from rest_framework.permissions import IsAuthenticated


# Create your views here.
# Create your views here.
@login_required(login_url='login')
def home(request):
    template_name = 'master/dashboard.html'
    context = {}
    return render(request, template_name,context)


class Branch_List(View):
    template_name = 'master/branch_list.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        branch_li = BranchMaster.objects.filter()
        context = {'branch_li': branch_li}
        return render(request, self.template_name, context)

class Branch_Create(View):
    template_name = 'master/branch_create.html'
    form_class = Branch_Create_Form

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
            branch = BranchMaster.objects.get(branch_id=data.branch_id) 
            username=request.POST.get('username')
            password=request.POST.get('pswd')
            hashed_password=make_password(password)
            email=data.email
            user_name=data.name
            branch_data=CustomUser.objects.create(password=hashed_password,username=username,first_name=user_name,email=email,user_type='Branch User',branch_id=branch)
            data.save()
            messages.success(request, 'Branch Successfully Added.', 'alert-success')
            return redirect('branch')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Field: {field}, Error: {error}")
            messages.success(request, 'Data is not valid.', 'alert-danger')
            context = {'form': form}
            return render(request, self.template_name, context)


class Branch_Edit(View):
    template_name = 'master/branch_edit.html'
    form_class = Branch_Edit_Form

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        rec = BranchMaster.objects.get(branch_id=pk)
        form = self.form_class(instance=rec)
        context = {'form': form,'rec':rec}
        return render(request, self.template_name, context)
 
    @method_decorator(login_required)
    def post(self, request, pk, *args, **kwargs):
        rec = BranchMaster.objects.get(branch_id=pk)
        form = self.form_class(request.POST, request.FILES, instance=rec)
        if form.is_valid():
            data = form.save(commit=False)
            print(request)
            data.modified_by = str(request.user.id)
            data.modified_date = datetime.now()
            data.save()
            messages.success(request, 'Branch Data Successfully Updated', 'alert-success')
            return redirect('branch')
        else:
            #print(form.errors)
            messages.success(request, 'Data is not valid.', 'alert-danger')
            context = {'form': form}
            return render(request, self.template_name, context)

class Branch_Details(View):
    template_name = 'master/branch_details.html'

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        branch_det = BranchMaster.objects.get(branch_id=pk)
        context = {'branch_det': branch_det}
        return render(request, self.template_name, context)    

class Route_List(View):
    template_name = 'master/route_list.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        route_li = RouteMaster.objects.filter()
        context = {'route_li': route_li}
        return render(request, self.template_name, context)
    
class Route_Create(View):
    template_name = 'master/route_create.html'
    form_class = Route_Create_Form

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
            
            branch_id=request.user.branch_id.branch_id
            branch = BranchMaster.objects.get(branch_id=branch_id)  # Adjust the criteria based on your model
            data.branch_id = branch
            data.save()
            messages.success(request, 'Route Successfully Added.', 'alert-success')
            return redirect('route')
        else:
            #print(form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Field: {field}, Error: {error}")
            messages.success(request, 'Data is not valid.', 'alert-danger')
            context = {'form': form}
            return render(request, self.template_name, context)


class Route_Edit(View):
    template_name = 'master/route_edit.html'
    form_class = Route_Edit_Form

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        rec = RouteMaster.objects.get(route_id=pk)
        form = self.form_class(instance=rec)
        context = {'form': form,'rec':rec}
        return render(request, self.template_name, context)
    
    @method_decorator(login_required)
    def post(self, request, pk, *args, **kwargs):
        rec = RouteMaster.objects.get(route_id=pk)
        form = self.form_class(request.POST, request.FILES, instance=rec)
        if form.is_valid():
            data = form.save(commit=False)
            data.modified_by = str(request.user.id)
            data.modified_date = datetime.now()
            data.save()
            messages.success(request, 'Route Data Successfully Updated', 'alert-success')
            return redirect('route')
        else:
            #print(form.errors)
            messages.success(request, 'Data is not valid.', 'alert-danger')
            context = {'form': form}
            return render(request, self.template_name, context)

class Route_Details(View):
    template_name = 'master/route_details.html'

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        route_det = RouteMaster.objects.get(route_id=pk)
        context = {'route_det': route_det}
        return render(request, self.template_name, context)    

class Designation_List(View):
    template_name = 'master/designation_list.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        designation_li = DesignationMaster.objects.filter()
        context = {'designation_li': designation_li}
        return render(request, self.template_name, context)
    
class Designation_Create(View):
    template_name = 'master/designation_create.html'
    form_class = Designation_Create_Form

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
            messages.success(request, 'Designation Successfully Added.', 'alert-success')
            return redirect('designation')
        else:
            #print(form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Field: {field}, Error: {error}")
            messages.success(request, 'Data is not valid.', 'alert-danger')
            context = {'form': form}
            return render(request, self.template_name, context)

class Designation_Edit(View):
    template_name = 'master/designation_edit.html'
    form_class = Designation_Edit_Form

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        rec = DesignationMaster.objects.get(designation_id=pk)
        form = self.form_class(instance=rec)
        context = {'form': form,'rec':rec}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, pk, *args, **kwargs):
        rec = DesignationMaster.objects.get(designation_id=pk)
        form = self.form_class(request.POST, request.FILES, instance=rec)
        if form.is_valid():
            data = form.save(commit=False)
            data.modified_by = str(request.user.id)
            data.modified_date = datetime.now()
            data.save()
            messages.success(request, 'Designation Data Successfully Updated', 'alert-success')
            return redirect('designation')
        else:
            #print(form.errors)
            messages.success(request, 'Data is not valid.', 'alert-danger')
            context = {'form': form}
            return render(request, self.template_name, context)

class Designation_Details(View):
    template_name = 'master/designation_details.html'

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        designation_det = DesignationMaster.objects.get(designation_id=pk)
        context = {'designation_det': designation_det}
        return render(request, self.template_name, context)
    
def branch(request):
    context = {}
    return render(request, 'master/branch_list.html',context)
    
class Location_List(View):
    template_name = 'master/locations_list.html'

    def get(self, request, *args, **kwargs):
        location_li = LocationMaster.objects.all()
        context = {'location_li': location_li}
        return render(request, self.template_name, context)

class Location_Adding(View):
    template_name = 'master/location_add.html'
    form_class = Location_Add_Form

    def get(self, request, *args, **kwargs):
        emirate_values = EmirateMaster.objects.all()
        print(emirate_values)
        context = {'emirate_values': emirate_values}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        print(" check valid")
        try:
            if form.is_valid():
                data = form.save(commit=False)
                branch_id=request.user.branch_id.branch_id
                branch = BranchMaster.objects.get(branch_id=branch_id)
                data.branch_id = branch
                data.created_by = str(request.user)
                data.save()
                messages.success(request, 'Location Successfully Added.', 'alert-success')
                return redirect('locations_list')
            else:
                messages.success(request, 'Data is not valid.', 'alert-danger')
                context = {'form': form}
                return render(request, self.template_name, context)
        except Exception as e:
            print(":::::::::::::::::::::::",e)


class Location_Edit(View):
    template_name = 'master/location_edit.html'
    form_class = Location_Edit_Form

    def get(self, request, pk, *args, **kwargs):
        rec = LocationMaster.objects.get(location_id=pk)
        form = self.form_class(instance=rec)
        emirate_values = EmirateMaster.objects.all()  # Queryset for populating emirate dropdown
        context = {'form': form, 'emirate_values': emirate_values}
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        rec = LocationMaster.objects.get(location_id=pk)
        form = self.form_class(request.POST, request.FILES, instance=rec)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            messages.success(request, 'Location Data Successfully Updated', 'alert-success')
            return redirect('locations_list')
        else:
            #print(form.errors)
            messages.success(request, 'Data is not valid.', 'alert-danger')
            context = {'form': form}
            return render(request, self.template_name, context)


class Location_Delete(View):

    def get(self, request, pk, *args, **kwargs):
        rec = LocationMaster.objects.get(location_id=pk)
        return render(request, 'master/location_delete.html', {'location': rec})
    
    def post(self, request, pk, *args, **kwargs):
        rec = LocationMaster.objects.get(location_id=pk)
        rec.delete()
        messages.success(request, 'Location Data Deleted Successfully', 'alert-success')
        return redirect('locations_list')
    

        
class Category_List(View):
    template_name = 'master/category_list.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        category_li = CategoryMaster.objects.filter()
        context = {'category_li': category_li}
        return render(request, self.template_name, context)

class Category_Create(View):
    template_name = 'master/category_create.html'
    form_class = Category_Create_Form

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
            return redirect('category')
        else:
            #print(form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Field: {field}, Error: {error}")
            messages.success(request, 'Data is not valid.', 'alert-danger')
            context = {'form': form}
            return render(request, self.template_name, context)

class Category_Edit(View):
    template_name = 'master/category_edit.html'
    form_class = Category_Edit_Form

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        rec = CategoryMaster.objects.get(category_id=pk)
        form = self.form_class(instance=rec)
        context = {'form': form,'rec':rec}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, pk, *args, **kwargs):
        rec = CategoryMaster.objects.get(category_id=pk)
        form = self.form_class(request.POST, request.FILES, instance=rec)
        if form.is_valid():
            data = form.save(commit=False)
            data.modified_by = str(request.user.id)
            data.modified_date = datetime.now()
            data.save()
            messages.success(request, 'Category Data Successfully Updated', 'alert-success')
            return redirect('category')
        else:
            #print(form.errors)
            messages.success(request, 'Data is not valid.', 'alert-danger')
            context = {'form': form}
            return render(request, self.template_name, context)

class Category_Details(View):
    template_name = 'master/category_details.html'

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        category_det = CategoryMaster.objects.get(category_id=pk)
        context = {'category_det': category_det}
        return render(request, self.template_name, context)
    
# def create_emirates():
#     EmirateMaster.objects.create(created_by = "default",name = "Abudhabi")
#     EmirateMaster.objects.create(created_by = "default",name = "Dubai")
#     EmirateMaster.objects.create(created_by = "default",name = "Sharjah")
#     EmirateMaster.objects.create(created_by = "default",name = "Ajman")
#     EmirateMaster.objects.create(created_by = "default",name = "Fujeriah")
#     EmirateMaster.objects.create(created_by = "default",name = "RAK")
#     EmirateMaster.objects.create(created_by = "default",name = "UAQ")
# create_emirates()