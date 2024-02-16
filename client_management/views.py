from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import datetime
from django.contrib import messages
from django.shortcuts import render, redirect,HttpResponse
from django.views import View
import uuid
from .forms import  *
from accounts.models import *
from .models import *
from master.models import RouteMaster, LocationMaster
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from product.models import *
from django.db.models import Q
from sales_management.forms import CustomerCustodyForm, ProductForm



def customer_custody_item(request,customer_id):
    template_name = 'client_management/add_custody_items.html'
    if request.method == "GET":
        print(request.user.user_type,"<---user_type")
        customer_exists = Customers.objects.filter(customer_id=customer_id).exists()
        if customer_exists:
            customer_data = Customers.objects.get(pk=customer_id)
            if request.user.user_type == 'Admin':
                branch = BranchMaster.objects.all().values_list('branch_id', flat=True)
                print(branch,"<--branch")
                products = Product.objects.filter(branch_id__in=branch)

            else:
                branch_id=request.user.branch_id.branch_id
                branch = BranchMaster.objects.get(branch_id=branch_id)
                products = Product.objects.filter(branch_id=branch)
            print(products,"<--products")

            price_list = []
            for product in products:
                default_rates_exists = Product_Default_Price_Level.objects.filter(product_id=product,customer_type=customer_data.customer_type).exists()
                if default_rates_exists:
                    default_rates = Product_Default_Price_Level.objects.get(product_id=product,customer_type=customer_data.customer_type)
                    custody_items_exists = Customer_Custody_Items.objects.filter(product_id=product,customer=customer_data.customer_id).exists()
                    if custody_items_exists:
                        custody_items = Customer_Custody_Items.objects.get(product_id=product,customer=customer_data.customer_id)
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
                    custody_item_id = ''
                    product_id = product.product_id
                    product_name = product.product_name
                    product_rate = 0
                    product_count = 0

                ite = {'custody_item_id':custody_item_id,'product_id': product_id, 'product_name': product_name,'product_rate':product_rate,'product_count':product_count}
                price_list.append(ite)
        context = {'price_list': price_list,'customerid':customer_data.customer_id,'customername':customer_data.customer_name}
        return render(request, template_name, context)
    
    if request.method == 'POST':
        customer_id = request.POST.get('id_customer')
        product_ids = request.POST.getlist('price_checkbox')
        rate = request.POST.getlist('rate')
        count = request.POST.getlist('count')
        id_custody_items = request.POST.getlist('id_custody_item')
        if customer_id is not None and product_ids is not None:
            customer_instance = Customers.objects.get(pk=customer_id)
            for i, item_id in enumerate(product_ids):
                product_id, index = item_id.split('+')
                index = int(index) - 1

                product_instance = Product.objects.get(product_id=product_id)
                if id_custody_items[index]=='':
                    Customer_Custody_Items.objects.create(created_by=request.user,
                                        customer=customer_instance,
                                        rate=rate[index],
                                        count=count[index],
                                        product=product_instance)   
                else:
                    customer_custody_instance = Customer_Custody_Items.objects.get(custody_item_id=id_custody_items[index])
                    customer_custody_instance.rate = rate[index]
                    customer_custody_instance.count = count[index]
                    customer_custody_instance.save()

            messages.success(request, 'Custody Items Successfully Added.', 'alert-success')
            return redirect('customers')
        else:
            messages.success(request, 'Data is not valid.', 'alert-danger')
            context = {}
    return render(request, template_name, context)


#ajax
def get_custody_items(request):
    if request.method == "GET":
        customer = request.GET['customer']
        if customer is not None:
            customer_exists = Customers.objects.filter(customer_id=customer).exists()
            if customer_exists:
                customer_data = Customers.objects.get(pk=customer)
                branch_id=request.user.branch_id.branch_id
                branch = BranchMaster.objects.get(branch_id=branch_id)
                products = Product.objects.filter(branch_id=branch)
                price_list = []
                for product in products:
                   default_rates_exists = Product_Default_Price_Level.objects.filter(product_id=product,customer_type=customer_data.customer_type).exists()
                   if default_rates_exists:
                        default_rates = Product_Default_Price_Level.objects.get(product_id=product,customer_type=customer_data.customer_type)
                        custody_items_exists = Customer_Custody_Items.objects.filter(product_id=product,customer=customer_data.customer_id).exists()
                        if custody_items_exists:
                            custody_items = Customer_Custody_Items.objects.get(product_id=product,customer=customer_data.customer_id)
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
                        custody_items_exists = Customer_Custody_Items.objects.filter(product_id=product,customer=customer_data.customer_id).exists()
                        if custody_items_exists:
                            custody_items = Customer_Custody_Items.objects.get(product_id=product,customer=customer_data.customer_id)
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
    

class Custody_ItemListView(View):
    template_name = 'client_management/custody_item_list.html'
    def get(self, request):
        form = CustodyItemFilterForm(request.GET)
        customer_list = Customer_Custody_Items.objects.all()
        print('customer_list',customer_list)
       

        if form.is_valid():
            route_name = form.cleaned_data.get('route_name')
            if route_name:
                # Assuming the relationship is through a ForeignKey in the Customer model
                customer_ids = Customers.objects.filter(routes__route_name=route_name).values_list('customer_id', flat=True)
                # Filter using the correct field, which is 'customer_id__in'
                customer_list = customer_list.filter(customer_id__in=list(customer_ids))

                # customer_list = customer_list.filter(customer_id__in=customer_ids)
                print("customer_list",customer_list)

                return render(request, self.template_name, {'customer_list': customer_list, 'form': form})


    # def get(self, request):
    #     form = CustodyItemFilterForm(request.GET or None)
    #     customer_custody_list = Customer_Custody_Items.objects.all()
    #     print(customer_custody_list)

    #     customer_ids = []  # Define customer_ids here

    #     if form.is_valid():
    #         route_name = form.cleaned_data.get('route_name')
    #         if route_name:
    #             # Assuming the relationship is through a ForeignKey in the Customer model
    #             customer_ids = Customers.objects.filter(routes__route_name=route_name).values_list('customer_id', flat=True)
    #             # Filter using the correct field, which is 'customer_id__in'
    #             customer_custody_list = customer_custody_list.filter(customer_id__in=list(customer_ids))

    #     # Get the mobile number for each customer
    #     # mobile_numbers = {customer_id: customer.mobile_no for customer_id, customer in Customers.objects.in_bulk(customer_ids).items()}
    #     # print("mobile_numbers",mobile_numbers)
        return render(request, self.template_name, {'customer_list': customer_list, 'form': form})

from django.shortcuts import render, redirect
from .forms import CustomerCustodyItemsForm

def create_custody_item(request):
    if request.method == 'POST':
        form = CustomerCustodyItemsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('custody_item_list')  # Redirect to a success page
    else:
        form = CustomerCustodyItemsForm()
    return render(request, 'client_management/addcustodyitem.html', {'form': form})


    
class Add_CategoryListView(View):
    template_name = 'client_management/add_category_list.html'

    def get(self, request, pk, *args, **kwargs):
        user_det = Customers.objects.get(pk=pk)
        print(user_det)
        custody_items = Customer_Custody_Items.objects.filter(customer=user_det)
        form = CustomerCustodyForm()
        context = {
            'user_det': user_det,
            'custody_items': custody_items,
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        user_det = Customers.objects.get(pk=pk)
        category = request.POST.get('category')
        product_id = request.POST.get('product_name')
        print('product_name',product_id)
        drate = request.POST.get('drate')
        quantity = request.POST.get('quantity')
        serial_number = request.POST.get('serial_number')
        print("serial_number",serial_number)

        try:
            product = Product.objects.get(product_id=product_id)

            # If you are using product_id instead of product_name
            # product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)

        try:
            customer_custody_items = Customer_Custody_Items.objects.create(
                product=product,
                rate=drate,
                count=quantity,
                serialnumber=serial_number
            )
            # return JsonResponse({'success': 'customer custody items added successfully'}, status=200)
            return redirect('added_list')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
class AddListView(View):
    template_name = 'client_management/added_list.html'

    def get(self, request):
        get_addedlist=Customer_Custody_Items.objects.all()
        print('get_addedlist',get_addedlist)
        return render(request, self.template_name, {'get_addedlist': get_addedlist })


class Get_CategoryListView(View):
    def get(self, request):
        category_id = request.GET.get('category_id')
        products = Product.objects.filter(category_id=category_id).values('product_id', 'product_name','rate')
        return JsonResponse({'products': list(products)})

class GetRateView(View):
    def get(self, request):
        product_id = request.GET.get('product_id')
        print("product_id",product_id)
        try:
            print("tryyyyyy")
            product = Product.objects.get(pk=product_id)
            rate = product.rate
            return JsonResponse({'rate': rate})
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        
class PulloutListView(View):
    template_name = 'client_management/pullout_list.html'

    # def get(self, request):
        # form = CustodyItemFilterForm(request.GET)
    def get(self, request, pk):
        customer = Customers.objects.get(pk=pk)
        print('customer',customer)
        custody_items = Customer_Custody_Items.objects.filter(customer=customer)
        # custody_pullout_list = Customer_Custody_Items.objects.all()
        print("custody_pullout_list",list(custody_items))
        return render(request, self.template_name, {'custody_items': custody_items,'customer': customer})



