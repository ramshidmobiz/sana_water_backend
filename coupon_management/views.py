from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from competitor_analysis.forms import CompetitorAnalysisFilterForm
from master.functions import generate_form_errors
from .models import *
from .forms import  *
from accounts.models import CustomUser
from master.models import EmirateMaster,BranchMaster
import json
from django.core.serializers import serialize
from django.views import View
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

# Create your views here.

def couponType(request):
    all_couponType = CouponType.objects.all()
    context = {'all_couponType': all_couponType}
    return render(request, 'coupon_management/index_couponType.html', context)

def create_couponType(request):
    if request.method == 'POST':
        form = CreateCouponTypeForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.created_by = str(request.user.id)
            data.save()
            messages.success(request, 'Coupon Type created successfully!')
            return redirect('couponType')
        else:
            messages.error(request, 'Invalid form data. Please check the input.')
    else:
        form = CreateCouponTypeForm()
    context = {'form': form}
    return render(request, 'coupon_management/create_couponType.html', context)


def view_couponType(request, coupon_type_id):
    view_couponType = get_object_or_404(CouponType, coupon_type_id=coupon_type_id)
    return render(request, 'coupon_management/view_couponType.html', {'view_couponType': view_couponType})

def edit_CouponType(request, coupon_type_id):
    edit_coupon = get_object_or_404(CouponType, coupon_type_id=coupon_type_id)
    if request.method == 'POST':
        form = EditCouponTypeForm(request.POST, instance=edit_coupon)
        if form.is_valid():
            data = form.save(commit=False)
            # print(data,"data")
            data.modified_by = str(request.user.id)
            data.modified_date = datetime.now()
            data.save()
            return redirect('couponType')
    else:
        form = EditCouponTypeForm(instance=edit_coupon)
    return render(request, 'coupon_management/edit_couponType.html', {'form': form, 'edit_coupon': edit_coupon})

def delete_couponType(request, coupon_type_id):
    deleteCouponType = CouponType.objects.get(coupon_type_id=coupon_type_id)
    if request.method == 'POST':
        deleteCouponType.delete()
        return redirect('couponType')
    return render(request, 'coupon_management/delete_couponType.html', {'deleteCouponType': deleteCouponType})


################Add Coupon###########
def coupon(request):
    all_coupon = Coupon.objects.all()
    context = {'all_coupon': all_coupon}
    return render(request, 'coupon_management/index_coupon.html', context)

def create_coupon(request):
    if request.method == 'POST':
        form = CreateCouponForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.created_by = str(request.user.id)
            data.save()
            messages.success(request, 'Coupon created successfully!')
            return redirect('coupon')
        else:
            messages.error(request, 'Invalid form data. Please check the input.')
    else:
        form = CreateCouponForm()
    context = {'form': form}
    return render(request, 'coupon_management/create_coupon.html', context)

def view_coupon(request, coupon_id):
    view_coupon = get_object_or_404(Coupon, coupon_id=coupon_id)
    return render(request, 'coupon_management/view_coupon.html', {'view_coupon': view_coupon})

def edit_Coupon(request, coupon_id):
    edit_coupon = get_object_or_404(Coupon, coupon_id=coupon_id)
    if request.method == 'POST':
        form = EditCouponForm(request.POST, instance=edit_coupon)
        if form.is_valid():
            data = form.save(commit=False)
            # print(data,"data")
            data.modified_by = str(request.user.id)
            data.modified_date = datetime.now()
            data.save()
            return redirect('coupon')
    else:
        form = EditCouponForm(instance=edit_coupon)
    return render(request, 'coupon_management/edit_coupon.html', {'form': form, 'edit_coupon': edit_coupon})

def delete_coupon(request, coupon_id):
    deleteCoupon = Coupon.objects.get(coupon_id=coupon_id)
    if request.method == 'POST':
        deleteCoupon.delete()
        return redirect('coupon')
    return render(request, 'coupon_management/delete_coupon.html', {'deleteCoupon': deleteCoupon})

####              Coupon Request   ##############
# def couponrequest(request):
#     all_couponrequest = CouponRequest.objects.all()
#     context = {'all_couponrequest': all_couponrequest}
#     return render(request, 'coupon_management/index_couponRequest.html', context)

def couponrequest(request):
    all_couponrequest = CouponRequest.objects.all()

    for couponrequest in all_couponrequest:
        try:
            assign_staff_coupon = AssignStaffCoupon.objects.filter(coupon_request=couponrequest).first()
            couponrequest.assign_staff_coupon = assign_staff_coupon
            print("couponrequest.assign_staff_coupon",couponrequest.assign_staff_coupon)
        except AssignStaffCoupon.DoesNotExist:
            couponrequest.assign_staff_coupon = None
            print("DoesNotExist")

    context = {'all_couponrequest': all_couponrequest}
    return render(request, 'coupon_management/index_couponRequest.html', context)


def create_couponRequest(request):
    if request.method == 'POST':
        form = CouponRequestForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.created_by = str(request.user.id)
            if request.user.branch_id:
                try:
                    branch_id = request.user.branch_id.branch_id
                    branch = BranchMaster.objects.get(branch_id=branch_id)  
                    data.branch_id = branch
                    data.save()
                    messages.success(request, 'Coupon Request Created successfully!')
                    return redirect('couponrequest')
                except ObjectDoesNotExist:
                    # Handle the case where branch_id is not found
                    messages.error(request, 'Branch information not found for the current user.')
                    # You can also add additional handling or redirect logic here
            else:
                # Handle the case where branch_id is None
                messages.error(request, 'Branch information not found for the current user.')
                # You can also add additional handling or redirect logic here
        else:
            messages.error(request, 'Invalid form data. Please check the input.')
    else:
        form = CouponRequestForm()
    context = {'form': form}
    return render(request, 'coupon_management/create_couponRequest.html', context)



def view_couponRequest(request, coupon_request_id):
    view_couponRequest = get_object_or_404(CouponRequest, coupon_request_id=coupon_request_id)
    # print("view_couponRequest",view_couponRequest)
    

    return render(request, 'coupon_management/view_couponRequest.html', {'view_couponRequest': view_couponRequest})

#----------------------------AssignStaffCoupon--------------------------#
def assignStaffCoupon(request):
    all_assignStaffCoupon = AssignStaffCoupon.objects.all()
    # print("all_assignStaffCoupon",all_assignStaffCoupon)
    context = {'all_assignStaffCoupon': all_assignStaffCoupon}
    return render(request, 'coupon_management/index_assignStaffCoupon.html', context)

def assign_to_staff(request, coupon_request_id):
    assign = get_object_or_404(CouponRequest, coupon_request_id=coupon_request_id)
    
    coupon_type = assign.coupon_type_id
    quantity = assign.quantity
    branch_id = assign.branch_id
    coupon_request=assign.coupon_request_id
    
    if request.method == 'POST':
        form = AssignStaffCouponForm(request.POST)
        # print("form",form)
        if form.is_valid():
            # Get the AssignStaffCoupon instance from the form
            # print("VALID")
            data = form.save(commit=False)

            # Compare alloted_quantity with remaining_quantity and update status
            alloted_quantity = int(data.alloted_quantity)
            data.remaining_quantity=int(quantity)-alloted_quantity

            # Compare remaining_quantity with quantity and set status
            # data.status = 'Closed' if data.remaining_quantity <= 0 else 'Pending'
            data.status = 'Pending' if data.remaining_quantity > 0 else 'Closed'

            

            # print("data.status",data.status)
            
            # Set other fields such as created_by, modified_by, etc.
            coupon_request_instance = get_object_or_404(CouponRequest, coupon_request_id=coupon_request)

            data.coupon_request=coupon_request_instance
            data.created_by = str(request.user.id)
            data.modified_by = str(request.user.id)
            data.modified_date = datetime.now()
            data.created_date = datetime.now()
            # Set other fields as needed...

            # Save the instance
            data.save()

            return redirect('couponrequest')  # Redirect to a success page or another URL
    else:
        form = AssignStaffCouponForm()
    

    
    
    return render(request, 'coupon_management/create_assignStaffCoupon.html', {
        'coupon_type': coupon_type,
        'quantity': quantity,
        'branch_id':branch_id,
        'form':form,
        'assign':assign
        
    })


def view_assignStaffCoupon(request, assign_id):
    view_assignStaffCoupon = get_object_or_404(AssignStaffCoupon, assign_id=assign_id)
    # print("view_couponRequest",view_couponRequest)
    

    return render(request, 'coupon_management/view_assignStaffCoupon.html', {'view_assignStaffCoupon': view_assignStaffCoupon})

#---------------------------------------ASSIGN CUSTOMER COUPON---------------------------------------------------------------------

from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, FormView
from django.urls import reverse_lazy
from datetime import datetime
from .forms import AssignStaffCouponDetailsForm

from django.contrib import messages

class AssignToCustomerView(FormView):
    template_name = 'coupon_management/assign_to_customer.html'
    form_class = AssignStaffCouponDetailsForm
    success_url = reverse_lazy('couponrequest')

    def get(self, request, *args, **kwargs):
        assign_to_customer = get_object_or_404(AssignStaffCoupon, assign_id=self.kwargs['assign_id'])
        return render(request, self.template_name, {
            'assign_to_customer': assign_to_customer,
            'assign_id': assign_to_customer.assign_id,
            'coupon_request': assign_to_customer.coupon_request,
            'quantity': assign_to_customer.coupon_request.quantity,
            'branch_id': assign_to_customer.coupon_request.branch_id,
            'alloted_quantity': assign_to_customer.alloted_quantity,
            'form': self.get_form(),
        })

    def form_valid(self, form):
        assign_to_customer = get_object_or_404(AssignStaffCoupon, assign_id=self.kwargs['assign_id'])
        data = form.save(commit=False)
        
        if isinstance(self.request.user, CustomUser):
            data.created_by = str(self.request.user.id)
            data.modified_by = str(self.request.user.id)
        else:
            messages.error(self.request, 'Only The Staff User can Permitted for This')
            return self.form_invalid(form)
        
        data.modified_date = datetime.now()
        data.created_date = datetime.now()
        data.staff_coupon_assign = assign_to_customer
        
        # Check the status of AssignStaffCoupon
        if assign_to_customer.status == 'Closed':
            data.status = 'Assigned To Staff'
        else:
            # Check if to_customer is selected
            if data.to_customer:
                data.status = 'Assigned To Customer'
            else:
                data.status = 'Pending'
                
        data.save()
        return super().form_valid(form)

    
class AssignStaffCouponDetailsListView(View):
    template_name = 'coupon_management/coupon_details_view_list.html'

    def get(self, request):
        assign_staff_coupon_details_list = AssignStaffCouponDetails.objects.all()
        context = {
            'assign_staff_coupon_details_list': assign_staff_coupon_details_list,
          
        }
        return render(request, self.template_name, context)
#------------------------New Coupon
def new_coupon(request):
    all_coupon = NewCoupon.objects.all()
    coupon_stock_list = CouponStock.objects.all()  # Fetch all CouponStock instances
    context = {'all_coupon': all_coupon, 'coupon_stock_list': coupon_stock_list}  # Add coupon_stock_list to context
    return render(request, 'coupon_management/index_Newcoupon.html', context)

def create_Newcoupon(request):
    if request.method == 'POST':
        form = CreateNewCouponForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            
            coupon_type_id = request.POST.get('coupon_type')
            book_num = request.POST.get('book_num')
            
            # Check if the coupon book already exists
            if NewCoupon.objects.filter(book_num=book_num,coupon_type=coupon_type_id).exists():
                print("Exists")
                messages.error(request, f'Coupon book {book_num} already exists.')
                return redirect('new_coupon')
            selected_coupon_type = get_object_or_404(CouponType, coupon_type_id=coupon_type_id)

            data.coupon_type = selected_coupon_type
            data.book_num = book_num
            data.no_of_leaflets = selected_coupon_type.no_of_leaflets
            data.valuable_leaflets = selected_coupon_type.valuable_leaflets
            data.free_leaflets = selected_coupon_type.free_leaflets
            data.created_by = str(request.user.id)
            branch_id = request.user.branch_id.branch_id
            branch = BranchMaster.objects.get(branch_id=branch_id)
            data.branch_id = branch           
            data.save()
            print("DATA SAVED")

            # Generate leaflets for the coupon
            leaflets = []
            no_of_leaflets = int(selected_coupon_type.no_of_leaflets)
            print("no_of_leaflets",no_of_leaflets)
            for leaflet_num in range(1, no_of_leaflets + 1):
                if leaflet_num < 10:  # If leaflet number is less than 10, add a leading '0'
                    leaflet_name = f"{book_num}0{leaflet_num}"
                else:
                    leaflet_name = f"{book_num}{leaflet_num}"  # Otherwise, use leaflet_num directly
                print("leaflet_name", leaflet_name)

                leaflet = CouponLeaflet(coupon=data, leaflet_number=str(leaflet_num),leaflet_name=leaflet_name)
                print("leaflet",leaflet)
                leaflet.save()
                leaflets.append({'leaflet_number': leaflet.leaflet_number})
            # Create CouponStock instance
            coupon_stock = CouponStock.objects.create(couponbook=data, coupon_stock='company', created_by=str(request.user.id))
            # print("coupon_stock",coupon_stock)

            response_data = {
                'success': True,
                'book_num': data.book_num,
                'leaflets': leaflets
            }
            return JsonResponse(response_data, status=200)
        
        else:
            message = generate_form_errors(form,formset=False)
            response_data = {
                'success': False, 
                'message': message,
                }
            return JsonResponse(response_data, status=200)
    else:
        form = CreateNewCouponForm()
    
    context = {'form': form}
    return render(request, 'coupon_management/create_Newcoupon.html', context)

def generate_leaflets(request, coupon_id):
    coupon = get_object_or_404(NewCoupon, coupon_id=coupon_id)
    leaflets = []
    no_of_leaflets = int(coupon.coupon_type.no_of_leaflets)
    for leaflet_num in range(1, no_of_leaflets + 1):
        leaflet = CouponLeaflet(coupon=coupon, leaflet_number=str(leaflet_num))
        print("leaflet",leaflet)
        leaflets.append(leaflet)
        leaflet.save()
        

    context = {'coupon': coupon, 'leaflets': leaflets}
    return render(request, 'coupon_management/create_Newcoupon.html', context)

def get_leaflet_serial_numbers(request):
    if request.method == 'GET':
        coupon_type_id = request.GET.get('coupon_type')
        print("coupon_type_id",coupon_type_id)

        # Fetch leaflets based on the provided coupon type
        try:
            leaflets = CouponLeaflet.objects.filter(coupon__coupon_type_id=coupon_type_id)
            print("leaflets",leaflets)
            leaflet_data = [{'leaflet_number': leaflet.leaflet_number, 'is_used': leaflet.used} for leaflet in leaflets]
            print("leaflet_data",leaflet_data)
            return JsonResponse(leaflet_data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    

def save_coupon_data(request):
    if request.method == 'POST':
        form = CreateNewCouponForm(request.POST)
        if form.is_valid():
            try:
                # Save the coupon data to the database
                new_coupon = form.save()
                # You can also save leaflet data here if necessary
                return JsonResponse({'message': 'Coupon data saved successfully'})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Invalid form data'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def view_Newcoupon(request, coupon_id):
    view_coupon = get_object_or_404(NewCoupon, coupon_id=coupon_id)
    return render(request, 'coupon_management/view_Newcoupon.html', {'view_coupon': view_coupon})

def edit_NewCoupon(request, coupon_id):
    edit_coupon = get_object_or_404(NewCoupon, coupon_id=coupon_id)
    if request.method == 'POST':
        form = EditNewCouponForm(request.POST, instance=edit_coupon)
        if form.is_valid():
            data = form.save(commit=False)
            # print(data,"data")
            data.modified_by = str(request.user.id)
            data.modified_date = datetime.now()
            data.save()
            return redirect('new_coupon')
    else:
        form = EditNewCouponForm(instance=edit_coupon)
    return render(request, 'coupon_management/edit_Newcoupon.html', {'form': form, 'edit_coupon': edit_coupon})

def delete_Newcoupon(request, coupon_id):
    deleteCoupon = NewCoupon.objects.get(coupon_id=coupon_id)
    if request.method == 'POST':
        deleteCoupon.delete()
        return redirect('new_coupon')
    return render(request, 'coupon_management/delete_Newcoupon.html', {'deleteCoupon': deleteCoupon})

