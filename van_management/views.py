from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Van, Van_Routes, Van_License
from accounts.models import CustomUser, Customers
from master.models import EmirateMaster, RouteMaster
from customer_care.models import DiffBottlesModel
from client_management.models import Vacation

from .forms import  *
import json
from django.core.serializers import serialize
from django.views import View
from datetime import datetime
from collections import defaultdict
from reportlab.pdfgen import canvas
import pandas as pd
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from django.db.models import Q



# Van
def van(request):
    all_van = Van.objects.all()
    context = {'all_van': all_van}
    return render(request, 'van_management/van.html', context)

def create_van(request):
    if request.method == 'POST':
        form = VanForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.branch_id = request.user.branch_id
            data.created_by = str(request.user.id)
            data.save()
            messages.success(request, 'Van created successfully!')
            return redirect('van')
        else:
            messages.error(request, 'Invalid form data. Please check the input.')
    else:
        form = VanForm()
    context = {'form': form}
    return render(request, 'van_management/create_van.html', context)

def edit_van(request, van_id):
    van = get_object_or_404(Van, van_id=van_id)
    if request.method == 'POST':
        form = EditVanForm(request.POST, instance=van)
        if form.is_valid():
            data = form.save(commit=False)
            data.modified_by = str(request.user.id)
            data.modified_date = datetime.now()
            data.save()
            return redirect('van')
    else:
        form = EditVanForm(instance=van)
    return render(request, 'van_management/edit_van.html', {'form': form, 'van': van})

def view_van(request, van_id):
    van = get_object_or_404(Van, van_id=van_id)
    return render(request, 'van_management/view_van.html', {'van': van})

def delete_van(request, van_id):
    van = Van.objects.get(van_id=van_id)
    if request.method == 'POST':
        van.delete()
        return redirect('van')
    return render(request, 'master/confirm_delete.html', {'van': van})



# Van staff assigning
def view_association(request):
    vans_with_associations = Van.objects.exclude(driver=None).exclude(salesman=None)
    return render(request, 'van_management/driver_salesman_list.html', {'vans_with_associations': vans_with_associations})

def create_association(request):
    if request.method == 'POST':
        form = VanAssociationForm(request.POST)
        if form.is_valid():
            van_instance = form.cleaned_data['van']
            driver_id = form.cleaned_data['driver']
            salesman_id = form.cleaned_data['salesman']
            van = get_object_or_404(Van, van_id=van_instance.van_id)
            driver_instance = get_object_or_404(CustomUser, id=driver_id)
            salesman_instance = get_object_or_404(CustomUser, id=salesman_id)
            van.driver = driver_instance
            van.salesman = salesman_instance
            van.save()
            return redirect('/van_assign')
    else:
        form = VanAssociationForm()
    return render(request, 'van_management/create_assign.html', {'form': form})


def edit_assign(request, van_id):
    van = get_object_or_404(Van, van_id=van_id)
    if request.method == 'POST':
        form = EditAssignForm(van, request.POST)
        if form.is_valid(): 
            driver_id = form.cleaned_data['driver']
            salesman_id = form.cleaned_data['salesman']
            driver_instance = get_object_or_404(CustomUser, id=driver_id)
            salesman_instance = get_object_or_404(CustomUser, id=salesman_id)
            van.driver = driver_instance
            van.salesman = salesman_instance
            van.save()
            return redirect('/van_assign')
    else:
        form = EditAssignForm(van)

    return render(request, 'van_management/edit_assign.html', {'form': form, 'van': van})



def delete_assign(request, van_id):
    van = Van.objects.get(van_id=van_id)
    if request.method == 'POST':
        van.driver = None
        van.salesman = None
        van.save()
        return redirect('/van_assign')
    return render(request, 'master/confirm_delete_assign.html', {'van': van})

def route_assign(request,van_id):
    form = VanAssignRoutesForm()
    all_van=Van_Routes.objects.filter(van__van_id = van_id)
    van_data = Van.objects.get(van_id = van_id)
    context = {'all_van' : all_van,"form":form,"van_data":van_data}
    
    if request.method == 'POST':
        form = VanAssignRoutesForm(request.POST)
        context = {'all_van' : all_van,"form":form,"van_data":van_data}
        if form.is_valid():
            data = form.save(commit=False)
            route = data.routes
            route_exists = Van_Routes.objects.filter(van = van_data,routes = route).exists()
            if route_exists:
                messages.success(request, 'Route is already assigned..')
                context = {'all_van' : all_van,"form":form,"van_data":van_data}
                return render(request, 'van_management/assignroute_tovan.html',context)
            data.van = van_data
            data.created_by = str(request.user)
            data.created_date = datetime.now()
            data.save()
            messages.success(request, 'Van Route Assigned successfully!')
            return redirect('route_assign',van_id)
        else:
            messages.success(request, 'Invalid form data. Please check the input.')
            return render(request, 'van_management/assignroute_tovan.html',context)
    return render(request, 'van_management/assignroute_tovan.html',context)

def delete_route_assign (request):
    van_route_id = request.POST.get('delete_id')
    van_id = request.POST.get('van_idd')
    van = Van_Routes.objects.get(van_route_id=van_route_id)
    if request.method == 'POST':
        van.delete()
        return redirect('route_assign',van_id)
    return render(request, 'master/confirm_delete.html',{'van': van} )





class Licence_List(View):
    template_name = 'van_management/licence_list.html'
    
    def get(self, request, *args, **kwargs):
        emirates = EmirateMaster.objects.all().order_by('emirate_id')
        licenses = Van_License.objects.all()
        vans = {}
        emirate_names = [emirate.name for emirate in emirates]  # List to store emirate names dynamically

        for license in licenses:
            van_plate = license.van.plate
            emirate_name = license.emirate.name
            emirate_id = license.emirate.emirate_id
            expiry_date = license.expiry_date
        license_list = []
        for license in licenses:
            lic= {'license_id':license.van_license_id,'van_plate':license.van.plate,
                   'emirate_name':license.emirate,"expiry_date":license.expiry_date}
            license_list.append(lic)

            if van_plate not in vans:
                vans[van_plate] = {emirate: None for emirate in emirate_names}
            vans[van_plate][emirate_name] = expiry_date
        return render(request, self.template_name, {'vans': vans, 'emirate_names': emirate_names,'license_list':license_list})
    

class Licence_Adding(View):
    template_name = 'van_management/licence_add.html'
    form_class = Licence_Add_Form

    def get(self, request, *args, **kwargs):
        emirate_values = EmirateMaster.objects.all()
        van = Van.objects.all()
        context = {'emirate_values': emirate_values, 'vans': van}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit = False )
            van_id = request.POST.get('van')
            license_no = request.POST.get('licence_no')
            emirate_id = request.POST.get('emirate')
            expiry_date = request.POST.get('expiry_date')
            van = Van.objects.get(van_id = van_id)
            emirate = EmirateMaster.objects.get(pk = emirate_id)
            data.created_by = str(request.user.id)
            data.license_no = license_no
            data.van = van
            data.emirate = emirate
            data.expiry_date = expiry_date
            data.save()
            messages.success(request, 'Licence Successfully Added.', 'alert-success')
            return redirect('licence_list')
        else:
            messages.success(request, 'Data is not valid.', 'alert-danger')
            context = {'form': form}
            return render(request, self.template_name, context)
        
class License_Edit(View):
    template_name = 'van_management/licence_edit.html'
    form_class = Licence_Edit_Form

    def get(self, request, pk, *args, **kwargs):
        rec = Van_License.objects.get(van_license_id=pk)
        form = self.form_class(instance=rec)
        context = {'form': form,'rec':rec}
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        rec = Van_License.objects.get(van_license_id=pk)
        form = self.form_class(request.POST, request.FILES, instance=rec)
        if form.is_valid():
            data = form.save(commit=False)
            data.modified_by = str(request.user.id)
            data.modified_date = datetime.now()
            data.save()
            messages.success(request, 'Licence Successfully Updated', 'alert-success')
            return redirect('licence_list')
        else:
            messages.success(request, 'Data is not valid.', 'alert-danger')
            context = {'form': form}
            return render(request, self.template_name, context)
        
def licence_edit(request, plate):
    van = get_object_or_404(Van, plate=plate)
    van_id = van.van_id
    van_licence = Van_License.objects.filter(van=van)
    emirate = EmirateMaster.objects.all()
    if request.method == 'POST':
        emirate_id = request.POST.get('emirate')
        expiry_date = request.POST.get('expiry_date')
        existing_van_licence = Van_License.objects.filter(van=van, emirate_id=emirate_id).first()
        if existing_van_licence:
            existing_van_licence.expiry_date = expiry_date
            existing_van_licence.save()
        else:
            Van_License.objects.create(van=van, emirate_id=emirate_id, expiry_date=expiry_date)
        return redirect('licence_list')
    return render(request, 'van_management/licence_edit.html', {'emirate_values' : emirate})

# Need to remove 
def licence_delete(request, plate):
    van = get_object_or_404(Van, plate=plate)
    if request.method == 'POST':

        van = get_object_or_404(Van, plate=plate)
        van_id = van.van_id
        van_licence = Van_License.objects.filter(van_id = van_id)
        van_licence.delete()
        return redirect('licence_list')
    return render(request, 'master/licence_delete.html', {'van' : van})


# Trip schedule
def schedule_view(request):
    if request.method == 'POST':
        date_str = request.POST.get('date')
        if date_str:
            date = datetime.strptime(date_str, '%Y-%m-%d')
        
        routes = RouteMaster.objects.all()
        route_trip_details = []
        route_details=[]
        
        for route in routes:
            trip_count = 0
            customer_count = 0
            bottle_count=0
            todays_customers = find_customers(request, date_str, route.route_id)
            trips=[]
            for customer in todays_customers:
                customer_count+=1
                bottle_count+=customer['no_of_bottles']
                if customer['trip'] not in trips:
                    trips.append(customer['trip'])
            if bottle_count > 0:
                route_details.append({
                    'route_name':route.route_name,
                    'route_id':route.route_id,
                    'no_of_customers':customer_count,
                    'no_of_bottles':bottle_count,
                    'no_of_trips':len(trips),
                    'trips': trips
                })


        # for route in routes:
        #     todays_route_wise_customers = find_customers(request, date_str, route.route_id)
        #     if todays_route_wise_customers:
        #         trips = set(customer['trip'] for customer in todays_route_wise_customers)
        #         for trip in trips:
        #             trip_customers = [customer['customer_name'] for customer in todays_route_wise_customers if customer['trip'] == trip]
        #             route_trip_details.append({
        #                 'route_id': route.route_id,
        #                 'route_name': route.route_name,
        #                 'trip': trip,
        #                 'customers': trip_customers,
        #             })
        #     else:
        #         route_trip_details.append({
        #             'route_id': route.route_id,
        #             'route_name': route.route_name,
        #             'trip': 'No trip',  # Indicate no trip
        #             'customers': []  # Indicate no customers
        #         })
        
        return render(request, 'van_management/schedule_view.html', {'def_date':date_str, 'details':route_details})
        # return render(request, 'van_management/schedule_view.html', {'def_date':date_str, 'details':route_trip_details})
    return render(request, 'van_management/schedule_view.html')

            
def schedule_by_route(request, def_date, route_id, trip):
    route = RouteMaster.objects.get(route_id = route_id)
    todays_customers = find_customers(request, def_date, route_id)
    customers = []
    for customer in todays_customers:
        if customer['trip'] == trip:
            customers.append(customer)
    totale_bottle=0
    for customer in customers:
        totale_bottle+=customer['no_of_bottles']
    return render(request, 'van_management/schedule_by_route.html', {'def_date':def_date,  'route':route, 'todays_customers' :customers, 'trip':trip, 'totale_bottle':totale_bottle })
    


def find_customers(request, def_date, route_id):
    date_str = def_date
    if date_str:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        day_of_week = date.strftime('%A')
        week_num = (date.day - 1) // 7 + 1
        week_number = f'Week{week_num}'
    route = RouteMaster.objects.get(route_id=route_id)

    todays_customers = []

    buildings = []
    for customer in Customers.objects.filter(routes = route):
        if customer.visit_schedule and day_of_week in customer.visit_schedule and week_number in customer.visit_schedule[day_of_week]:
            todays_customers.append(customer)
            if customer.building_name not in buildings:
                buildings.append(customer.building_name)

    # Customers on vacation
    date = datetime.strptime(def_date, '%Y-%m-%d').date()
    for vacation in Vacation.objects.all():
        if vacation.start_date <= date <= vacation.end_date:
            if vacation.customer in todays_customers:
                todays_customers.remove(vacation.customer)

    # Emergency customer
    special_customers = DiffBottlesModel.objects.filter(delivery_date = date)
    emergency_customers = []
    for client in special_customers:
        if client.customer in todays_customers:
            emergency_customers.append(client.customer)
        else:
            if client.customer.routes == route:
                todays_customers.append(client.customer)
                emergency_customers.append(client.customer)
                if client.customer.building_name not in buildings:
                    buildings.append(client.customer.building_name)

    

    building_count = {}
    for building in buildings:
        for customer in todays_customers:
            if customer.building_name == building:
                if building in building_count:
                    building_count[building] += customer.no_of_bottles_required
                else:
                    building_count[building] = customer.no_of_bottles_required
    sorted_building_count = dict(sorted(building_count.items(), key=lambda item: item[1]))

    trips = {}
    trip_count = 1
    current_trip_bottle_count = 0
    trip_buildings = []

    for building, bottle_count in sorted_building_count.items():
        if current_trip_bottle_count + bottle_count > 200:
            trip_buildings = [building]
            trips[f"Trip{trip_count+1}"] = trip_buildings
            current_trip_bottle_count = bottle_count
        else:
            trip_buildings.append(building)
            trips[f"Trip{trip_count}"] = trip_buildings
            current_trip_bottle_count += bottle_count
        
    # List to store trip-wise customer details
    trip_customers = []
    for trip in trips:
        for customer in todays_customers:
            if customer.building_name in trips[trip]:
                trip_customer = {
                    "customer_name" : customer.customer_name,
                    "trip":trip,
                    "building":customer.building_name,
                    "route" : customer.routes.route_name,
                    "no_of_bottles": customer.no_of_bottles_required,
                    "location" : customer.location,
                }
                if customer in emergency_customers:
                    trip_customer['type'] = 'Emergency'
                else:
                    trip_customer['type'] = 'Default'
                trip_customers.append(trip_customer)
    return trip_customers

# pdf and excel

def pdf_download(request, route_id, def_date, trip):
    route = RouteMaster.objects.get(route_id=route_id)
    customers = []
    todays_customers = find_customers(request, def_date, route_id)
    for customer in todays_customers:
        if customer['trip'] == trip:
            customers.append(customer)

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    x_route_name, y_route_name = 80, 730
    formatted_date = datetime.strptime(def_date, '%Y-%m-%d').strftime('%d/%m/%Y')
    p.setFont("Helvetica", 14)
    p.drawString(x_route_name, y_route_name, f"Client list for {route.route_name} --> {trip}")
    p.drawString(x_route_name + 380, y_route_name, f"{formatted_date}")
    line_y = y_route_name - 14
    p.line(x_route_name - 12, line_y, x_route_name + 450, line_y)

    x, y = 70, 700
    p.setFont("Helvetica", 9)
    p.drawString(x, y, "Si No")
    p.drawString(x + 30, y, "Client Name")
    p.drawString(x + 135, y, "Location")
    p.drawString(x + 200, y, "No of Bottles")
    p.drawString(x + 267, y, "Outstanding")
    p.drawString(x + 280, y-10, "Bottles")
    p.drawString(x + 330, y, "Outstanding")
    p.drawString(x + 337, y-10, "Coupons")
    p.drawString(x + 400, y, "Type")
    y -= 16
    p.line(x, y, x + 460, y)

    y -= 15

    counter = 1
    for customer in customers:
        if customer['type'] == 'Emergency':
            p.setFillColorRGB(140, 0, 0)
            p.drawString(x, y, str(counter))
            p.drawString(x+30, y, str(customer['customer_name']))
            p.drawString(x + 120, y, str(customer['location']))
            p.drawString(x + 220, y, str(customer['no_of_bottles']))
            p.drawString(x + 300, y, "")
            p.drawString(x + 350, y, "")
            p.drawString(x + 400, y, "Emergency")
            y -= 20
            counter += 1
        else:
            p.setFillColorRGB(0, 0, 0)
            p.drawString(x, y, str(counter))
            p.drawString(x+30, y, str(customer['customer_name']))
            p.drawString(x + 120, y, str(customer['location']))
            p.drawString(x + 220, y, str(customer['no_of_bottles']))
            p.drawString(x + 300, y, "")
            p.drawString(x + 350, y, "")
            p.drawString(x + 400, y, "Default")
            y -= 20
            counter += 1
    if counter == 1:
        p.setFont("Helvetica", 11)
        p.drawString(x + 150 , y-60, "No Clients in this Route Today")

    p.showPage()
    p.save()
    buffer.seek(0)

    filename = f"{route.route_name}_{def_date}_{trip}.pdf"
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response
    


def excel_download(request, route_id, def_date, trip):
    route = RouteMaster.objects.get(route_id=route_id)
    customers = []
    todays_customers = find_customers(request, def_date, route_id)
    
    # Manually generate serial numbers
    serial_number = 1
    for customer in todays_customers:
        if customer['trip'] == trip:
            customer['serial_number'] = serial_number
            customers.append(customer)
            serial_number += 1  # Increment serial number

    data = {
        'Serial Number': [customer['serial_number'] for customer in customers],
        'Client Name': [customer['customer_name'] for customer in customers],
        'Locations': [customer['location'] for customer in customers],
        'No of Bottles': [customer['no_of_bottles'] for customer in customers],
        'Outstanding Bottles': ['' for _ in customers],
        'Outstanding Coupons': ['' for _ in customers],
        'Type': [customer['type'] for customer in customers]
    }

    df = pd.DataFrame(data)
    buffer = BytesIO()
    df.to_excel(buffer, index=False, engine='openpyxl')
    buffer.seek(0)

    filename = f"{route.route_name}_{def_date}_{trip}.xlsx"
    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response