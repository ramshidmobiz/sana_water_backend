import uuid
import json
import datetime

from django.views import View
from django.db.models import Q
from django.urls import reverse
from django.contrib import messages
from django.db import transaction, IntegrityError
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render

from .forms import  *
from .models import *
from product.models import *
from accounts.models import *
from master.functions import generate_form_errors
from master.models import RouteMaster, LocationMaster
# from sales_management.forms import CustomerCustodyForm, ProductForm

from django.template.loader import get_template
from xhtml2pdf import pisa
from openpyxl import Workbook
from openpyxl.styles import Alignment
from competitor_analysis.forms import CompetitorAnalysisFilterForm
from django.db.models import Q


def customer_custody_item(request,customer_id):
    customer_instance = Customers.objects.get(customer_id=customer_id)
    CustodyItemsFormset = formset_factory(CustodyCustomItemForm, extra=2)
    
    message = ''
    if request.method == 'POST':
        custody_custom_form = CustodyCustomForm(request.POST)
        custody_items_formset = CustodyItemsFormset(request.POST,prefix='custody_items_formset', form_kwargs={'empty_permitted': False})
        
        if custody_custom_form.is_valid() and custody_items_formset.is_valid():
            try:
                with transaction.atomic():
                    custody_custom_data = custody_custom_form.save(commit=False)
                    custody_custom_data.created_by=request.user.id
                    custody_custom_data.created_date=datetime.today()
                    custody_custom_data.modified_by=request.user.id
                    custody_custom_data.modified_date=datetime.today()
                    
                    custody_custom_data.customer=customer_instance
                    custody_custom_data.save()
                    
                    for form in custody_items_formset:
                        item = form.save(commit=False)
                        item.custody_custom = custody_custom_data
                        item.save()
                    response_data = {
                        "status": "true",
                        "title": "Successfully Created",
                        "message": "custody Item created successfully.",
                        'redirect': 'true',
                        "redirect_url": reverse('customers')
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
            message = generate_form_errors(custody_custom_form, formset=False)
            message += generate_form_errors(custody_items_formset, formset=True)
            
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    
    else:
        custody_custom_form = CustodyCustomForm()
        custody_items_formset = CustodyItemsFormset(prefix='custody_items_formset')
        
        context = {
            'custody_custom_form': custody_custom_form,
            'custody_items_formset': custody_items_formset,
            'customer_instance' : customer_instance,
            
            'page_title': 'Create Custody Item',
            'page_name' : 'create Custody Item',
        }
        
        return render(request,'client_management/add_custody_items.html',context)


# def customer_custody_item(request,customer_id):
#     template_name = 'client_management/add_custody_items.html'
#     if request.method == "GET":
#         customer_exists = Customers.objects.filter(customer_id=customer_id).exists()
#         if customer_exists:
#             customer_data = Customers.objects.get(customer_id=customer_id)
#             products = ProdutItemMaster.objects.all()

#             price_list = []
#             for product in products:
#                 default_rates_exists = Product_Default_Price_Level.objects.filter(product_id=product,customer_type=customer_data.customer_type).exists()
#                 if default_rates_exists:
#                     default_rates = Product_Default_Price_Level.objects.get(product_id=product,customer_type=customer_data.customer_type)
#                     custody_items_exists = CustodyCustomItems.objects.filter(product_id=product,customer=customer_data.customer_id).exists()
#                     if custody_items_exists:
#                         custody_items = CustodyCustomItems.objects.get(product_id=product,customer=customer_data.customer_id)
#                         custody_item_id = custody_items.custody_item_id
#                         product_id = product.pk
#                         product_name = product.product_name
#                         product_rate = custody_items.rate
#                         product_count = custody_items.count
#                     else:
#                         custody_item_id = ''
#                         product_id = product.pk
#                         product_name = product.product_name
#                         product_rate = default_rates.rate
#                         product_count = 0
#                 else:
#                     custody_item_id = ''
#                     product_id = product.pk
#                     product_name = product.product_name
#                     product_rate = 0
#                     product_count = 0

#                 ite = {'custody_item_id':custody_item_id,'product_id': product_id, 'product_name': product_name,'product_rate':product_rate,'product_count':product_count}
#                 price_list.append(ite)
#         context = {'price_list': price_list,'customerid':customer_data.customer_id,'customername':customer_data.customer_name}
#         return render(request, template_name, context)
    
#     if request.method == 'POST':
#         customer_id = request.POST.get('id_customer')
#         product_ids = request.POST.getlist('price_checkbox')
#         rate = request.POST.getlist('rate')
#         count = request.POST.getlist('count')
#         id_custody_items = request.POST.getlist('id_custody_item')
#         if customer_id is not None and product_ids is not None:
#             customer_instance = Customers.objects.get(customer_id=customer_id)
#             for i, item_id in enumerate(product_ids):
#                 product_id, index = item_id.split('+')
#                 index = int(index) - 1

#                 product_instance = ProdutItemMaster.objects.get(pk=product_id)
#                 if id_custody_items[index]=='':
#                     CustodyCustomItems.objects.create(created_by=request.user,
#                                         customer=customer_instance,
#                                         rate=rate[index],
#                                         count=count[index],
#                                         product=product_instance)   
#                 else:
#                     customer_custody_instance = CustodyCustomItems.objects.get(custody_item_id=id_custody_items[index])
#                     customer_custody_instance.rate = rate[index]
#                     customer_custody_instance.count = count[index]
#                     customer_custody_instance.save()

#             messages.success(request, 'Custody Items Successfully Added.', 'alert-success')
#             return redirect('customers')
#         else:
#             messages.success(request, 'Data is not valid.', 'alert-danger')
#             context = {}
#     return render(request, template_name, context)


#ajax
def get_custody_items(request):
    if request.method == "GET":
        customer = request.GET['customer']
        if customer is not None:
            customer_exists = Customers.objects.filter(customer_id=customer).exists()
            if customer_exists:
                customer_data = Customers.objects.get(customer_id=customer)
                branch_id=request.user.branch_id.branch_id
                branch = BranchMaster.objects.get(branch_id=branch_id)
                products = Product.objects.filter(branch_id=branch)
                price_list = []
                for product in products:
                   default_rates_exists = Product_Default_Price_Level.objects.filter(product_id=product,customer_type=customer_data.customer_type).exists()
                   if default_rates_exists:
                        default_rates = Product_Default_Price_Level.objects.get(product_id=product,customer_type=customer_data.customer_type)
                        custody_items_exists = CustodyCustomItems.objects.filter(product_id=product,customer=customer_data.customer_id).exists()
                        if custody_items_exists:
                            custody_items = CustodyCustomItems.objects.get(product_id=product,customer=customer_data.customer_id)
                            custody_item_id = custody_items.custody_item_id
                            product_id = product.product_id
                            product_name = product.product_name
                            product_rate = custody_items.rate
                            product_count = custody_items.count
                        else:
                            custody_item_id = ''
                            product_id = product.product_id
                            product_name = product.product_name
                            product_rate = default_rates.rate
                            product_count = 0
                   else:
                        custody_items_exists = CustodyCustomItems.objects.filter(product_id=product,customer=customer_data.customer_id).exists()
                        if custody_items_exists:
                            custody_items = CustodyCustomItems.objects.get(product_id=product,customer=customer_data.customer_id)
                            custody_item_id = custody_items.custody_item_id
                            product_id = product.product_id
                            product_name = product.product_name
                            product_rate = custody_items.rate
                            product_count = custody_items.count
                        else:
                            custody_item_id = ''
                            product_id = product.product_id
                            product_name = product.product_name
                            product_rate = default_rates.rate
                            product_count = 0

                   ite = {'custody_item_id':custody_item_id,'product_id': product_id, 'product_name': product_name,'product_rate':product_rate,'product_count':product_count}
                   price_list.append(ite)
            dat = {'price_list': price_list}   
        return JsonResponse(dat)
    
    # --------------------------------------------------------------------------

# Vaccation
def vacation_list(request):
    template = 'client_management/vacation_list.html'
    Vacation.objects.filter(end_date__lt= date.today()).delete()
    vacation = Vacation.objects.all()
    context = {'vacation':vacation}
    return render(request, template, context)

class RouteSelection(View):
    def get(self, request):
        template = 'client_management/select_route.html'
        routes = RouteMaster.objects.all()
        return render(request, template, {'routes': routes}) 
    
class Vacation_Add(View):
    def get(self, request):
        template = 'client_management/vacation_add.html'
        form = Vacation_Add_Form
        search_form = CustomerSearchForm()
        selected_route = request.GET.get('route')
        print('root',selected_route)
        customers = Customers.objects.filter(routes = selected_route)
        search_query = request.GET.get('search_query')
        if search_query:
            customers = customers.filter(
                Q(customer_name__icontains=search_query) |
                Q(mobile_no__icontains=search_query) |
                Q(location__location_name__icontains=search_query) |
                Q(building_name__icontains=search_query) 
            )
        return render(request, template, {'form': form, 'search_form': search_form, 'customers': customers, 'selected_route':selected_route})

    def post(self, request):
        template = 'client_management/vacation_add.html'
        form = Vacation_Add_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect(vacation_list)
        return render(request, template, {'form': form})
    
class Vacation_Edit(View):
    template = 'client_management/vacation_edit.html'
    def get(self, request, vacation_id):
        vacation = Vacation.objects.get(vacation_id=vacation_id)
        form = Vacation_Edit_Form(instance=vacation)
        return render(request, self.template, {'form': form, 'vacation': vacation})

    def post(self, request, vacation_id):
        vacation = Vacation.objects.get(vacation_id=vacation_id)
        form = Vacation_Edit_Form(request.POST, instance=vacation)
        if form.is_valid():
            form.save()
            return redirect(vacation_list)
        return render(request, self.template, {'form': form, 'vacation': vacation})

class Vacation_Delete(View):
    template='client_management/vacation_delete.html'
    def get(self, request, vacation_id):
        vacation = Vacation.objects.get(vacation_id=vacation_id)
        return render(request, self.template, {'vacation':vacation})

    def post(self, request, vacation_id):
        vacation = Vacation.objects.get(vacation_id=vacation_id)
        vacation.delete()
        return redirect(vacation_list)
    


class CustomerCustodyList(View):
    template_name = 'client_management/custody_item/customer_custody_list.html'

    def get(self, request, *args, **kwargs):
        form = CompetitorAnalysisFilterForm(request.GET)
        
        user_li = CustodyCustomItems.objects.all()
        query = request.GET.get("q")
        if query:
            user_li = user_li.filter(
                Q(custody_custom__customer__customer_name__icontains=query)|
                Q(custody_custom__customer__mobile_no__icontains=query)|
                Q(custody_custom__customer__building_name__icontains=query)|
                Q(custody_custom__customer__routes__route_name__icontains=query)

            )
            

        route_filter = request.GET.get('route_name')
        if route_filter:
            user_li = user_li.filter(custody_custom__route__route_name=route_filter)

        # Fetch counts of 5 gallons, dispenser, and water cooler from Product model
        five_gallon_count = Product.objects.filter(product_name__product_name='5 Gallon').count()
        dispenser_count = Product.objects.filter(product_name__product_name='Dispenser').count()
        water_cooler_count = Product.objects.filter(product_name__product_name='Water Cooler').count()

        context = {
            'user_li': user_li,
            'form': form,
            'five_gallon_count': five_gallon_count,
            'dispenser_count': dispenser_count,
            'water_cooler_count': water_cooler_count,
        }
        return render(request, self.template_name, context)       


class AddCustodyItems(View):
    template_name = 'client_management/custody_item/add_custody_items.html'
    form_class = CustodyCustomItemForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            # Save the instance based on deposit_form value
            # if instance.deposit_form:
            #     instance.amount = instance.deposit_amount
            #     instance.deposit_form_number = instance.deposit_number
            # else:
            #     instance.amount = None
            instance.save()
            messages.success(request, 'Entry created successfully!')
            return redirect('add_custody_list')
        return render(request, self.template_name, {'form': form})

        
class AddCustodyList(View):
    template_name = 'client_management/custody_item/add_custody_list.html'

    def get(self, request):
        get_addedlist = CustodyCustomItems.objects.all()
        print(get_addedlist,'geddedlist')
        return render(request, self.template_name, {'get_addedlist': get_addedlist })
    
class EditCustodyItem(View):
    template_name = 'client_management/custody_item/add_custody_list.html'

    def get(self, request):
        get_addedlist = CustodyCustomItems.objects.all()
        print(get_addedlist,'geddedlist')
        return render(request, self.template_name, {'get_addedlist': get_addedlist })



class PulloutListView(View):
    template_name = 'client_management/pullout_list.html'

    # def get(self, request):
        # form = CustodyItemFilterForm(request.GET)
    def get(self, request, pk):
        customer = Customers.objects.get(customer_id=pk)
        print('customer',customer)
        custody_items = CustodyCustomItems.objects.filter(customer=customer)
        # custody_pullout_list = Customer_Custody_Items.objects.all()
        print("custody_pullout_list",list(custody_items))
        return render(request, self.template_name, {'custody_items': custody_items,'customer': customer})
    

@login_required
def customer_supply_list(request):
    """
    Customer Supply List
    :param request:
    :return: CustomerSupplys list view
    """
    
    instances = CustomerSupply.objects.all().order_by("-created_date")
         
    date_range = ""
    date_range = request.GET.get('date_range')
    # print(date_range)

    if date_range:
        start_date_str, end_date_str = date_range.split(' - ')
        start_date = datetime.strptime(start_date_str, '%m/%d/%Y').date()
        end_date = datetime.strptime(end_date_str, '%m/%d/%Y').date()
        instances = instances.filter(date__range=[start_date, end_date])
    
    filter_data = {}
    query = request.GET.get("q")
    
    if query:

        instances = instances.filter(
            Q(customer_supply_no__icontains=query) |
            Q(product__customer_supply_id__icontains=query) 
        )
        title = "Customer Supply List - %s" % query
        filter_data['q'] = query
    
    context = {
        'instances': instances,
        'page_name' : 'Customer Supply List',
        'page_title' : 'Customer Supply List',
        'filter_data' :filter_data,
        'date_range': date_range,
        
        'is_customer_supply': True,
        'is_need_datetime_picker': True,
    }

    return render(request, 'client_management/customer_supply/list.html', context)

@login_required
def customer_supply_customers(request,pk):
    filter_data = {}
    
    instances = Customers.objects.all()
    
    if request.GET.get('route'):
        instances = instances.filter(routes__pk=request.GET.get('route'))
        
    if request.GET.get('building_no'):
        instances = instances.filter(door_house_no=request.GET.get('building_no'))
    
    query = request.GET.get("q")
    
    if query:

        instances = instances.filter(
            Q(customer_id__icontains=query) |
            Q(mobile_no__icontains=query) |
            Q(whats_app__icontains=query) |
            Q(customer_name__icontains=query) 
        )
        title = "Customer Supply Customers - %s" % query
        filter_data['q'] = query
        
    route_instances = RouteMaster.objects.all()

    context = {
        'instances': instances,
        'route_instances' : route_instances,
        
        'page_title': 'Create customer supply',
        'customer_supply_page': True,
        'is_need_datetime_picker': True
    }
    
    return render(request,'client_management/customer_supply/customer_list.html',context)

def create_customer_supply(request):
    
    message = ''
    if request.method == 'POST':
        customer_supply_form = CustomerSupplyForm(request.POST)
        customer_supply_items_form = CustomerSupplyItemsForm(request.POST)
        
        if customer_supply_form.is_valid() and customer_supply_items_form.is_valid():
            try:
                with transaction.atomic():
                    customer_supply = customer_supply_form.save(commit=False)
                    customer_supply.created_by = str(request.user.id)
                    customer_supply.save()
                    
                    data = customer_supply_items_form.save(commit=False)
                    data.customer_supply = customer_supply
                    data.save()
                    
                    if (update_customer_stock:=CustomerSupplyStock.objects.filter(customer=customer_supply.customer,product=data.product)).exists():
                            stock = update_customer_stock.first()
                            stock.stock_quantity += data.quantity
                            stock.save()
                    else:
                        CustomerSupplyStock.objects.create(
                            product=data.product,
                            customer=customer_supply.customer,
                            stock_quantity = data.quantity,
                        )
                    
                    response_data = {
                        "status": "true",
                        "title": "Successfully Created",
                        "message": "Customer Supply created successfully.",
                        'redirect': 'true',
                        "redirect_url": reverse('customer_supply:customer_supply_list')
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
            message = generate_form_errors(customer_supply_form,formset=False)
            message += generate_form_errors(customer_supply_items_form,formset=False)
            
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    
    else:
        customer_supply_form = CustomerSupplyForm()
        customer_supply_items_form = CustomerSupplyItemsForm()
        
        context = {
            'customer_supply_form': customer_supply_form,
            'customer_supply_items_form': customer_supply_items_form,
            
            'page_title': 'Create customer supply',
            'customer_supply_page': True,
            'is_need_datetime_picker': True
        }
        
        return render(request,'client_management/customer_supply/create.html',context)


@login_required
def edit_customer_supply(request,pk):
    """
    edit operation of customer_supply
    :param request:
    :param pk:
    :return:
    """
    customer_supply_instance = CustomerSupply.objects.get(pk=pk)
    message = ''
    
    if request.method == 'POST':
        customer_supply_form = CustomerSupplyForm(request.POST,instance=customer_supply_instance)
        customer_supply_items_form = CustomerSupplyItemsForm(request.POST,instance=customer_supply_instance)            
        
        if customer_supply_form.is_valid() and  customer_supply_items_form.is_valid() :
            #create
            data = customer_supply_form.save(commit=False)
            data.save()
            
            for form in customer_supply_items_form:
                if form not in customer_supply_items_form.deleted_forms:
                    i_data = form.save(commit=False)
                    if not i_data.customer_supply :
                        i_data.customer_supply = customer_supply_instance
                    i_data.save()

            for f in customer_supply_items_form.deleted_forms:
                f.instance.delete()
                
            response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "customer supply Updated Successfully.",
                'redirect': 'true',
                "redirect_url": reverse('customer_supply:customer_supply_list'),
                "return" : True,
            }
    
        else:
            message = generate_form_errors(customer_supply_form,formset=False)
            message += generate_form_errors(customer_supply_items_form,formset=False)
            
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
                        
    else:
        customer_supply_form = CustomerSupplyForm()
        customer_supply_items_form = CustomerSupplyItemsForm()

        context = {
            'customer_supply_form': customer_supply_form,
            'customer_supply_items_form': customer_supply_items_form,
            
            'message': message,
            'page_name' : 'edit customer supply',
            'customer_supply_page': True,   
            'is_edit' : True,        
        }

        return render(request, 'client_management/customer_supply/create.html', context)
    
@login_required
def delete_customer_supply(request, pk):
    """
    customer_supply deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    customer_supply = CustomerSupply.objects.filter(pk=pk)
    CustomerSupplyItems.objects.filter(customer_supply__pk=pk).delete()
    customer_supply.delete()
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "customer supply Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('customer_supply:customer_supply_list'),
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


#------------------------------REPORT----------------------------------------

def client_report(request):
    instances = Customers.objects.order_by('-created_date')  # Order by latest created date
    return render(request, 'client_management/client_report.html', {'instances': instances})


def clientdownload_pdf(request, customer_id):
    customer = get_object_or_404(Customers, pk=customer_id)
    template_path = 'client_management/client_report_pdf.html'
    context = {'customer': customer}

    # Logic to generate PDF for the specific customer
    pdf_content = f"PDF content for {customer.customer_name}"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{customer.customer_name}_report.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    # Create PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response


def clientexport_to_csv(request, customer_id):
    customer = get_object_or_404(Customers, pk=customer_id)

    # Create an Excel workbook and select the active sheet
    wb = Workbook()
    ws = wb.active

    # Set the title
    title_cell = ws.cell(row=1, column=1, value="Client Details")
    title_cell.alignment = Alignment(horizontal='center')  # Align the title to the center
    ws.merge_cells('A1:F1')  # Merge cells for the title

    # Define data to be written
    data = [
        ['Customer Name:', customer.customer_name],
        ['Address:', f"{customer.building_name} {customer.door_house_no}"],
        ['Contact:', customer.mobile_no],
        ['Customer Type:', customer.customer_type],
        ['Sales Type:', customer.sales_type],
    ]

    # Write data to the worksheet
    for row in data:
        ws.append(row)

    # Set response headers for Excel file download
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{customer.customer_name}_report.xlsx"'

    # Save the workbook to the HttpResponse
    wb.save(response)

    return response


def custody_items_list_report(request):
    if request.method == 'GET':
        
        instances = CustodyCustom.objects.all()
        # if start_date_str and end_date_str:
        #     start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        #     end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        #     instances = CustodyCustomItems.objects.filter(custody_custom__created_date__range=[start_date, end_date])
        # else:
        
        return render(request, 'client_management/custody_items_list_report.html', {'instances': instances})
    



