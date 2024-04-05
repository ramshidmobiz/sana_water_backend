# views.py
import json
import random
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.views import View
from django.shortcuts import render
from django.db.models import Q
from client_management.models import CustodyCustomItems
from coupon_management.models import AssignStaffCouponDetails
from master.models import RouteMaster  # Assuming you have imported RouteMaster
from accounts.models import Customers
from product.models import Product, Product_Default_Price_Level
from sales_management.models import OutstandingLog
from tax_settings.models import Tax
from .forms import SaleEntryFilterForm
from django.views.generic import FormView, View
from django.http import JsonResponse
from django.urls import reverse_lazy
from .forms import CashCustomerSaleForm, CreditCustomerSaleForm, CashCouponCustomerSaleForm, CreditCouponCustomerSaleForm
from accounts.models import Customers
import random
import string
from django.db.models import Sum
from django.views.generic import View
from django.shortcuts import render, redirect
from django.db.models import Sum
from .models import  OutstandingLog, SaleEntryLog, SalesExtraModel, SalesTemp, Transaction
from accounts.models import Customers
from .forms import ProductForm  # Import the ProductForm we created earlier
from django.db.models import F, Value
from django.db.models.functions import Coalesce
from django.views.generic import ListView
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from io import BytesIO  

from .models import *
from client_management.models import *
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import xlsxwriter
from .models import *
from openpyxl import Workbook
import pandas as pd
from io import BytesIO
from reportlab.pdfgen import canvas
from django.utils import timezone

class TransactionHistoryListView(ListView):
    model = Transaction
    template_name = 'sales_management/transaction_history.html'  # Update with your actual template path
    context_object_name = 'transaction_history_list'

class SaleEntryLogListView(ListView):
    model = SaleEntryLog
    template_name = 'sales_management/sale_entry_history.html'
    context_object_name = 'sale_entry_logs'

class OutstandingLogListView(ListView):
    model = OutstandingLog
    template_name = 'sales_management/oustanding_history.html'  # Update with your actual template path
    context_object_name = 'outstanding_logs'

# views.py

from django.http import JsonResponse

def payment_submit(request):
    if request.method == 'POST' and request.is_ajax():
        # Retrieve form data
        total_amount = request.POST.get('total_amount')
        discount = request.POST.get('discount')
        net_taxable = request.POST.get('net_taxable')
        vat = request.POST.get('vat')
        total_to_collect = request.POST.get('total_to_collect')
        amount_received = request.POST.get('amount_received')
        balance = request.POST.get('balance')

        # Print or process the form data as needed
        print("Total Amount:", total_amount)
        print("Discount:", discount)
        print("Net Taxable:", net_taxable)
        print("VAT:", vat)
        print("Total to Collect:", total_to_collect)
        print("Amount Received:", amount_received)
        print("Balance:", balance)

        # Return a JSON response
        return JsonResponse({'message': 'Payment data received successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


class SaleEntryLogView(View):
    template_name = 'sales_management/add_sale_entry.html'

    def get(self, request, *args, **kwargs):
        # Create an instance of the form and populate it with GET data
        form = SaleEntryFilterForm(request.GET)

        # Initialize not_found to False
        not_found = False

        # Check if the form is valid
        if form.is_valid():
            # Filter the queryset based on the form data
            route_filter = form.cleaned_data.get('route_name')
            search_query = form.cleaned_data.get('search_query')

            user_li = Customers.objects.all()

            if route_filter:
                user_li = user_li.filter(routes__route_name=route_filter)

            if search_query:
                # Apply search filter on relevant fields of the Customers model
                user_li = user_li.filter(
                    Q(customer_name__icontains=search_query) |
                    Q(building_name__icontains=search_query) |
                    Q(door_house_no__icontains=search_query)
                    # Add more fields as needed
                )

            # Check if the filtered data is empty
            not_found = not user_li.exists()

        else:
            # If the form is not valid, retrieve all customers
            user_li = Customers.objects.all()

        context = {'user_li': user_li, 'form': form, 'not_found': not_found}
        return render(request, self.template_name, context)
    
class CustomerDetailsView(View):
    template_name = 'sales_management/customer_sales_detail.html'

    def get(self, request, pk, *args, **kwargs):
        # Retrieve user details
        user_det = Customers.objects.get(customer_id=pk)
        sales_type = user_det.sales_type
        
        # Retrieve visit schedule data from user details
        visit_schedule_data = user_det.visit_schedule

        if visit_schedule_data:
            # Define a dictionary to map week names to numbers
            week_mapping = {"week1": 1, "week2": 2, "week3": 3, "week4": 4}

            # Initialize an empty list to store the result
            result = []

            # Loop through each day and its associated weeks
            for day, weeks in visit_schedule_data.items():
                for week in weeks:
                    # Extract week number using the week_mapping dictionary
                    week_number = week_mapping.get(week)
                    # Append day, week number, and day name to the result list
                    result.append((day, week_number))

            # Sort the result by week number
            result.sort(key=lambda x: x[1])

            # Prepare data for rendering
            data_for_rendering = []
            for slno, (day, week_number) in enumerate(result, start=1):
                data_for_rendering.append({'slno': slno, 'week': week_number, 'day': day})
        else:
            # If visit_schedule_data is None, handle it appropriately
            data_for_rendering = []

        # Filter AssignStaffCouponDetails based on customer_id
        assign_staff_coupon_details = AssignStaffCouponDetails.objects.filter(
            to_customer_id=user_det.customer_id
        )

        # Join AssignStaffCouponDetails with AssignStaffCoupon and aggregate the sum of remaining_quantity
        total_remaining_quantity = assign_staff_coupon_details.aggregate(
            total_remaining_quantity=Sum('staff_coupon_assign__remaining_quantity')
        )

        # Extract the sum of remaining_quantity from the aggregation result
        sum_remaining_quantity_coupons = total_remaining_quantity.get('total_remaining_quantity', 0)

        # Fetch all data from CustodyCustomItems model related to the user
        custody_items = CustodyCustomItems.objects.filter(customer=user_det)

        # Aggregate sum of coupons, empty bottles, and cash from OutstandingLog
        outstanding_log_aggregates = OutstandingLog.objects.filter(customer=user_det).aggregate(
            total_coupons=Sum('coupons'),
            total_empty_bottles=Sum('empty_bottles'),
            total_cash=Sum('cash')
        )
        # Check if all values in outstanding_log_aggregates are None
        if all(value is None for value in outstanding_log_aggregates.values()):
            outstanding_log_aggregates = None

        # Prepare the product form
        product_form = ProductForm()

        # Remove the coupon_method field from the form if sale type is "CASH" or "CREDIT"
        if sales_type in ["CASH", "CREDIT"]:
            del product_form.fields['coupon_method']
        # Add custody_items and aggregated data to the context
        context = {
            'user_det': user_det,
            'visit_schedule_data': data_for_rendering,
            'custody_items': custody_items,
            'outstanding_log_aggregates': outstanding_log_aggregates,  # Add aggregated data to the context
            'product_form': product_form,  # Add the product form to the context
        }

        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        # print("dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd")
        # Retrieve user details
        user_det = Customers.objects.get(customer_id=pk)

        # Process product form submission
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            # Save the product form data
            product = product_form.save(commit=False)
            product.created_by = request.user.username  # Set the created_by field
            product.save()
            return redirect('customer_details', pk=pk)
        else:
            # If the form is not valid, re-render the page with the form errors
            context = {
                'user_det': user_det,
                'product_form': product_form,
                # Add other context data as needed
            }
            return render(request, self.template_name, context)

class GetProductsByCategoryView(View):
    def get(self, request):
        category_id = request.GET.get('category_id')
        print(category_id,'category_id')
        products = Product.objects.filter(category_id=category_id).values('product_id', 'product_name')
        print("productsproducts", products)
        return JsonResponse({'products': list(products)})
    


    

class InitiateSaleView(FormView, View):
    template_name = 'sales_management/customer_sale_form.html'
    success_url = reverse_lazy('sale_entry_log_view')

    def get_form_class(self, sales_type):
        if sales_type == 'CASH':
            return CashCustomerSaleForm
        elif sales_type == 'CREDIT':
            return CreditCustomerSaleForm
        elif sales_type == 'CASH COUPON':
            return CashCouponCustomerSaleForm
        elif sales_type == 'CREDIT COUPON':
            return CreditCouponCustomerSaleForm
        else:
            return None

    def get(self, request, *args, **kwargs):
        print("///////////////////////////////////////////////////////////////////////////")
        get_data = request.GET.dict()
        print("get_dataget_dataget_data", get_data)
        customer_id = request.GET.get('customer_id')
        product_id = request.GET.get('product_name')
        print("product_idproduct_id", product_id)
        coupon_method = request.GET.get('coupon_method')
        print("coupon_methodcoupon_method", coupon_method)
        # Fetch the customer object
        customer = Customers.objects.filter(customer_id=customer_id).first()
        # Check if the customer exists
        # Filter AssignStaffCouponDetails based on customer_id
        assign_staff_coupon_details = AssignStaffCouponDetails.objects.filter(
            to_customer_id=customer_id
        )

        # Join AssignStaffCouponDetails with AssignStaffCoupon and aggregate the sum of remaining_quantity
        total_remaining_quantity = assign_staff_coupon_details.aggregate(
            total_remaining_quantity=Sum('staff_coupon_assign__remaining_quantity')
        )

        # Extract the sum of remaining_quantity from the aggregation result
        sum_remaining_quantity_coupons = total_remaining_quantity.get('total_remaining_quantity', 0)

        print("sum_remaining_quantity_couponssum_remaining_quantity_coupons", sum_remaining_quantity_coupons)
        if customer:
            if coupon_method != 'digital' or customer.sales_type not in ['CREDIT COUPON', 'CASH COUPON']:
                # Get the sales type for the customer
                sales_type = customer.sales_type
                # Instantiate the appropriate form class based on sales type
                form_class = self.get_form_class(sales_type)
                if form_class:
                    form = form_class()
                    # test 
                else:
                    return JsonResponse({'error': 'Invalid sales type'}, status=400)

                return self.render_to_response({'sum_remaining_quantity_coupons': sum_remaining_quantity_coupons, 'sales_type': sales_type, 'customer_id': customer_id, 'product_id': product_id, 'form': form, 'coupon_method': coupon_method})
                
            # Return 404 if customer does not exist
            return JsonResponse({'error': 'digital coupon found'}, status=404)
                            
        # Return 404 if customer does not exist
        return JsonResponse({'error': 'Customer not found'}, status=404)



    def generate_invoice_number(self):
        # Generate a random 10-digit invoice number
        invoice_number = ''.join(random.choices(string.digits, k=10))
        
        # Check if the generated number is unique in Transaction table
        while Transaction.objects.filter(invoice_number=invoice_number).exists():
            # If not unique, generate a new invoice number
            invoice_number = ''.join(random.choices(string.digits, k=10))
        
        # Check if the generated number is unique in SalesTemp table
        while SalesTemp.objects.filter(invoice_number=invoice_number).exists():
            # If not unique, generate a new invoice number
            invoice_number = ''.join(random.choices(string.digits, k=10))
        
        return invoice_number
    
    def delete_sales_temp_data(self,invoice_number):
        try:
            sales_temp_entry = SalesTemp.objects.get(invoice_number=invoice_number)
            sales_temp_entry.delete()
            print("Data deleted successfully from SalesTemp table for invoice number:", invoice_number)
        except SalesTemp.DoesNotExist:
            print("No data found in SalesTemp table for invoice number:", invoice_number)

    
    def post(self, request, *args, **kwargs):
        sales_type = request.POST.get('sales_type')
        customer_id = request.POST.get('customer_id')
        product_id = request.POST.get('product_id')
        customer = Customers.objects.filter(customer_id=customer_id).first()
        product = Product.objects.filter(product_id=product_id).first()
        id_status = request.POST.get('status')
        # Get sales_type from form data
        print("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq", request.POST)
        print("id_statusid_statusid_status", id_status)
        # Instantiate the appropriate form class based on sales type
        form_class = self.get_form_class(sales_type)
        print("form_classform_class", form_class)
        if form_class:
            print("entry_________________!")
            form = form_class(request.POST)
            print("formform", form)
            # Convert form input values to integers
            qty_needed = int(request.POST.get('qty_needed', 0))
            no_of_coupons = int(request.POST.get('no_of_coupons', 0))
            coupon_variations = int(request.POST.get('coupon_variations', 0))
            print("coupon_variationscoupon_variations", coupon_variations)
            empty_bottles = int(request.POST.get('empty_bottles', 0))
            collected_bottles = int(request.POST.get('collected_bottles', 0))
            bottle_variations = int(request.POST.get('bottle_variations', 0))
            id_status = request.POST.get('status')
            invoice_number = self.generate_invoice_number()
            cash=0
            print("id_statusid_status", id_status)
            if id_status == 'PAID':
                print("eeeeeeeeeeeeeeeeeeeeeeeee")
                invoice_number=request.POST.get('invoice_number')
                sales_temp_data = SalesTemp.objects.get(invoice_number=invoice_number).data
                customer = Customers.objects.filter(customer_id=sales_temp_data['customer_id']).first()
                product = Product.objects.filter(product_id=sales_temp_data['product_id']).first()
                get_tax_percentage= Tax.objects.filter(name="vat").first()
                vat_value= get_tax_percentage/100
                print("__________________________________________________________________________________", invoice_number)
                print("sales_temp_datasales_temp_data", sales_temp_data)
                print("__________________________________________________________________________________")
                # Calculate data based on form fields
                total_amount = (qty_needed + no_of_coupons) * coupon_variations  # Dummy calculation for total_amount
                discount = total_amount * 0.1  # Dummy calculation for discount (10% of total_amount)
                net_taxable = total_amount - discount  # Dummy calculation for net_taxable
                vat = net_taxable * vat_value  # Dummy calculation for VAT (5% of net_taxable)
                received_amount = net_taxable - vat  # Dummy calculation for received_amount (net_taxable - VAT)
                balance = received_amount - total_amount  # Dummy calculation for balance (received_amount - total_amount)
                print("id_statusid_status", id_status)
                cash=total_amount
                # Generate initial invoice number
                try:
                    # Save data to Transaction model
                    transaction = Transaction.objects.create(
                        customer=customer,
                        category='INCOME',
                        amount=total_amount,
                        created_staff=request.user,
                        invoice_number=invoice_number,
                        transaction_category=id_status
                        # Add other fields as needed
                    )
                    # Save data to SaleEntryLog model
                    sale_entry = SaleEntryLog.objects.create(
                        customer=customer,
                        quantity=qty_needed,
                        total_amount=total_amount,
                        discount=discount,
                        net_taxable=net_taxable,
                        vat=vat,
                        received_amount=received_amount,
                        balance=balance,
                        product=product,
                        empty_bottles=empty_bottles,

                        # Add other fields as needed
                    )
                    # Create SalesExtraModel instance with the calculated values
                    sales_extra_model = SalesExtraModel.objects.create(
                        qty_needed=qty_needed,
                        no_of_coupons=no_of_coupons,
                        coupon_variations=coupon_variations,
                        empty_bottles=empty_bottles,
                        collected_bottles=collected_bottles,
                        bottle_variations=bottle_variations,
                        status=id_status,
                        order_number=sale_entry.order_number  # Assuming you want to link it with the same order number
                    )
                    # Create an entry in the OutstandingLog model
                    outstanding_log = OutstandingLog.objects.create(
                        customer_id=customer_id,
                        coupons=coupon_variations,
                        empty_bottles=bottle_variations,
                        cash=balance,
                        created_by=request.user  # Assuming you have a logged-in user
                    )

                    self.delete_sales_temp_data(invoice_number)

                    return HttpResponseRedirect(reverse('sale_entry_log_list'))

                except IntegrityError as e:
                    # Extract relevant information from the IntegrityError object
                    error_message = str(e)
                    # Return a JsonResponse with the error message and appropriate status code
                    return JsonResponse({'error': error_message}, status=400)

            if id_status == "FOC":
                print("FOC is working")
                try:
                    # Save data to Transaction model
                    transaction = Transaction.objects.create(
                        customer=customer,
                        category='EXPENSE',
                        amount=0,
                        created_staff=request.user,
                        invoice_number=invoice_number,
                        transaction_category=id_status
                        # Add other fields as needed
                    )
                    # Save data to SaleEntryLog model
                    sale_entry = SaleEntryLog.objects.create(
                        customer=customer,
                        quantity=qty_needed,
                        total_amount=0,
                        discount=0,
                        net_taxable=0,
                        vat=0,
                        received_amount=0,
                        balance=0,
                        product=product,
                        empty_bottles=empty_bottles,
                        # Add other fields as needed
                    )

                    # Create SalesExtraModel instance with the calculated values
                    sales_extra_model = SalesExtraModel.objects.create(
                        qty_needed=qty_needed,
                        no_of_coupons=no_of_coupons,
                        coupon_variations=coupon_variations,
                        empty_bottles=empty_bottles,
                        collected_bottles=collected_bottles,
                        bottle_variations=bottle_variations,
                        status=id_status,
                        order_number=sale_entry.order_number  # Assuming you want to link it with the same order number
                    )
                    outstanding_log = OutstandingLog.objects.create(
                        customer_id=customer_id,
                        coupons=coupon_variations,
                        empty_bottles=bottle_variations,
                        cash=0,
                        created_by=request.user  # Assuming you have a logged-in user
                    )

                    return HttpResponseRedirect(reverse('sale_entry_log_list'))

                except IntegrityError as e:
                    # Extract relevant information from the IntegrityError object
                    error_message = str(e)
                    # Return a JsonResponse with the error message and appropriate status code
                    return JsonResponse({'error': error_message}, status=400)
                
            if id_status == "PENDING":
                print("PENDING is working")
                try:
                    # Save data to Transaction model
                    transaction = Transaction.objects.create(
                        customer=customer,
                        category='INCOME',
                        amount=0,
                        created_staff=request.user,
                        invoice_number=invoice_number,
                        transaction_category=id_status
                        # Add other fields as needed
                    )
                    # Save data to SaleEntryLog model
                    sale_entry = SaleEntryLog.objects.create(
                        customer=customer,
                        quantity=qty_needed,
                        total_amount=0,
                        discount=0,
                        net_taxable=0,
                        vat=0,
                        received_amount=0,
                        balance=0,
                        product=product,
                        empty_bottles=empty_bottles,
                        # Add other fields as needed
                    )
                    return HttpResponseRedirect(reverse('sale_entry_log_list'))

                except IntegrityError as e:
                    # Extract relevant information from the IntegrityError object
                    error_message = str(e)
                    # Return a JsonResponse with the error message and appropriate status code
                    return JsonResponse({'error': error_message}, status=400)
                
                
            if id_status == "CUSTODY":
                print("CUSTODY is working")
                try:
                    # Save data to Transaction model
                    transaction = Transaction.objects.create(
                        customer=customer,
                        category='INCOME',
                        amount=0,
                        created_staff=request.user,
                        invoice_number=invoice_number,
                        transaction_category=id_status
                        # Add other fields as needed
                    )
                    # Save data to SaleEntryLog model
                    sale_entry = SaleEntryLog.objects.create(
                        customer=customer,
                        quantity=qty_needed,
                        total_amount=0,
                        discount=0,
                        net_taxable=0,
                        vat=0,
                        received_amount=0,
                        balance=0,
                        product=product,
                        empty_bottles=empty_bottles,
                        # Add other fields as needed
                    )
                    outstanding_log = OutstandingLog.objects.create(
                        customer_id=customer_id,
                        coupons=coupon_variations,
                        empty_bottles=bottle_variations,
                        cash=0,
                        created_by=request.user  # Assuming you have a logged-in user
                    )
                    return HttpResponseRedirect(reverse('sale_entry_log_list'))

                except IntegrityError as e:
                    # Extract relevant information from the IntegrityError object
                    error_message = str(e)
                    # Return a JsonResponse with the error message and appropriate status code
                    return JsonResponse({'error': error_message}, status=400)
            # else:
            #     # Print form name
            #     form_name = form.__class__.__name__  # Get the class name of the form
            #     print(f"{form_name} is not valid. Errors:")
            #     for field, errors in form.errors.items():
            #         print(f"- Field: {field}, Errors: {', '.join(errors)}")
            #     # Return a JsonResponse with the error message and appropriate status code
            #     return JsonResponse({'error': f'{form_name} is not valid'}, status=400)


        # Ensure that you return a response in all code paths
        return JsonResponse({'success': 'Sale entry created successfully'}, status=200)



from django.http import JsonResponse

class PaymentForm(View):
    template_name = 'sales_management/customer_sales_detail.html'

    def generate_invoice_number(self):
        # Generate a random 10-digit invoice number
        invoice_number = ''.join(random.choices(string.digits, k=10))
        # Check if the generated number is unique in Transaction table
        while Transaction.objects.filter(invoice_number=invoice_number).exists():
            # If not unique, generate a new invoice number
            invoice_number = ''.join(random.choices(string.digits, k=10))
        # Check if the generated number is unique in SalesTemp table
        while SalesTemp.objects.filter(invoice_number=invoice_number).exists():
            # If not unique, generate a new invoice number
            invoice_number = ''.join(random.choices(string.digits, k=10))        
        return invoice_number

    def post(self, request, *args, **kwargs):
        print("gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg", request.POST)
        # Retrieve data from the POST request
        customer_id = request.POST.get('customer_id')
        product_id = request.POST.get('product_id')
        sales_type = request.POST.get('sales_type')
        qty_needed = request.POST.get('qty_needed')
        empty_bottles = request.POST.get('empty_bottles')
        collected_bottles = request.POST.get('collected_bottles')
        status = request.POST.get('status')
        discount_percentage = float(request.POST.get('discount_percentage'))/100
        print('statusstatusstatusstatusstatus', status)
        invoice_number = self.generate_invoice_number()
        if status == "PAID":
            # Create a dictionary to store the data
            data = {
                'customer_id': customer_id,
                'product_id': product_id,
                'sales_type': sales_type,
                'qty_needed': qty_needed,
                'empty_bottles': empty_bottles,
                'collected_bottles': collected_bottles,
                'status': status,
                'discount_percentage': discount_percentage,
            }
            # Create an instance of SalesTemp model and save it to the database
            sales_temp = SalesTemp.objects.create(invoice_number=invoice_number, data=data)

        # Fetch the rate from the Customers table based on the customer_id
        customer = Customers.objects.filter(customer_id=customer_id).first()
        if customer:
            customer_type = customer.customer_type
            get_customer_default_price = Product_Default_Price_Level.objects.filter(customer_type=customer_type, product_id=product_id).first()
            if get_customer_default_price:
                rate = float(get_customer_default_price.rate)
            else:
                # Handle the case where the rate is not available
                return JsonResponse({'error': 'Rate not available for the customer and product'}, status=400)
            # Fetch tax options from the Tax model
            tax_options = Tax.objects.all().values_list('id', 'name')
            # Calculate the total_amount by multiplying rate with qty_needed
            # Add None at the beginning of the tax options list
            tax_options_list = list(tax_options)
            tax_options_list.insert(0, (None, 'None'))
            
            total_amount = float(qty_needed) * rate

            print("7//////////////////////////////////////////////////////")
            print("qty_needed", qty_needed, "rateraterate", rate)
            print("total_amounttotal_amount", total_amount, type(total_amount))
            print("discount_percentage", discount_percentage, type(discount_percentage))


            discount_amount = total_amount * discount_percentage
            net_taxable = total_amount - discount_amount
            # Calculate VAT (5% of total_amount
            # Query to retrieve product tax percentage
            product_tax_percentage = Product.objects.filter(product_id=product_id).annotate(
                tax_percentage=Coalesce(F('tax__percentage'), Value(0))
            ).values_list('tax_percentage', flat=True).first()

            vat_percentage=product_tax_percentage/100
            print("vat_percentage", vat_percentage)
            vat = total_amount * vat_percentage

            total_to_collect = total_amount + vat
            # Calculate total_to_collect (net_taxable plus VAT)
        else:
            # Handle the case where customer is not found
            return JsonResponse({'error': 'Customer not found'}, status=400)

        # Prepare the response data
        response_data = {
            'total_amount': total_amount,
            'discount_amount': discount_amount,
            'net_taxable':net_taxable,
            'total_to_collect': total_to_collect,
            'vat':vat,
            'invoice_number':invoice_number,
            'sales_type': sales_type,
            'status': status,
        }
        print("response_dataresponse_data", response_data)

        # Return the response
        return JsonResponse(response_data)


class CalculateTotaltoCollect(View):
    def get(self, request):
        print("colllectAmount__calc")
        vat_value = request.GET.get('vat_value')
        # products = Product.objects.filter(vat_value=vat_value).values('product_id', 'product_name')
        # print("productsproducts", products)
        return JsonResponse({'products': list(vat_value)})



# class CouponSaleView(View):
#     template_name = 'sales_management/coupon_sale.html'

#     def get(self, request, *args, **kwargs):
#         # Create an instance of the form and populate it with GET data
#         form = SaleEntryFilterForm(request.GET)

#         # Initialize not_found to False
#         not_found = False

#         # Check if the form is valid
#         if form.is_valid():
#             # Filter the queryset based on the form data
#             route_filter = form.cleaned_data.get('route_name')
#             search_query = form.cleaned_data.get('search_query')

#             user_li = Customers.objects.all()

#             if route_filter:
#                 user_li = user_li.filter(routes__route_name=route_filter)

#             if search_query:
#                 # Apply search filter on relevant fields of the Customers model
#                 user_li = user_li.filter(
#                     Q(customer_name__icontains=search_query) |
#                     Q(building_name__icontains=search_query) |
#                     Q(door_house_no__icontains=search_query)
#                     # Add more fields as needed
#                 )

#             not_found = not user_li.exists()

#         else:
#             # If the form is not valid, retrieve all customers
#             user_li = Customers.objects.all()

#         context = {'user_li': user_li, 'form': form, 'not_found': not_found}
#         return render(request, self.template_name, context)



#     def post(self, request, *args, **kwargs):
        
    
class CouponSaleView(View):
    template_name = 'sales_management/coupon_sale.html'

    def get(self, request, *args, **kwargs):
        # Create an instance of the form and populate it with GET data
        form = SaleEntryFilterForm(request.GET)

        # Initialize not_found to False
        not_found = False

        # Check if the form is valid
        if form.is_valid():
            # Filter the queryset based on the form data
            route_filter = form.cleaned_data.get('route_name')
            search_query = form.cleaned_data.get('search_query')

            user_li = Customers.objects.all()

            if route_filter:
                user_li = user_li.filter(routes__route_name=route_filter)

            if search_query:
                user_li = user_li.filter(
                    Q(customer_name__icontains=search_query) |
                    Q(building_name__icontains=search_query) |
                    Q(door_house_no__icontains=search_query)
                )

            not_found = not user_li.exists()

        else:
            user_li = CustomerCoupons.objects.filter()

        balance_coupons = user_li
        print(balance_coupons,'balance_coupons')

        # Get the manual book type last purchased
        # manual_book_type_last_purchased = user_li.latest('created_date').deposit_type

        context = {'user_li': user_li, 'form': form, 'not_found': not_found}
        return render(request, self.template_name, context)
    

class DetailsView(View):
    template_name = 'sales_management/detail.html'

    def get(self, request, pk, *args, **kwargs):
        # Retrieve user details
        user_det = Customers.objects.get(customer_id=pk)
        sales_type = user_det.sales_type
        
        # Retrieve visit schedule data from user details
        visit_schedule_data = user_det.visit_schedule

        if visit_schedule_data:
            # Define a dictionary to map week names to numbers
            week_mapping = {"week1": 1, "week2": 2, "week3": 3, "week4": 4}

            # Initialize an empty list to store the result
            result = []

            # Loop through each day and its associated weeks
            for day, weeks in visit_schedule_data.items():
                for week in weeks:
                    # Extract week number using the week_mapping dictionary
                    week_number = week_mapping.get(week)
                    # Append day, week number, and day name to the result list
                    result.append((day, week_number))

            # Sort the result by week number
            # result.sort(key=lambda x: x[1])

            # Prepare data for rendering
            data_for_rendering = []
            for slno, (day, week_number) in enumerate(result, start=1):
                data_for_rendering.append({'slno': slno, 'week': week_number, 'day': day})
        else:
            # If visit_schedule_data is None, handle it appropriately
            data_for_rendering = []

        # Filter AssignStaffCouponDetails based on customer_id
        assign_staff_coupon_details = AssignStaffCouponDetails.objects.filter(
            to_customer_id=user_det.customer_id
        )

        # Join AssignStaffCouponDetails with AssignStaffCoupon and aggregate the sum of remaining_quantity
        total_remaining_quantity = assign_staff_coupon_details.aggregate(
            total_remaining_quantity=Sum('staff_coupon_assign__remaining_quantity')
        )

        # Extract the sum of remaining_quantity from the aggregation result
        sum_remaining_quantity_coupons = total_remaining_quantity.get('total_remaining_quantity', 0)

        # Fetch all data from CustodyCustomItems model related to the user
        custody_items = CustodyCustomItems.objects.filter(customer=user_det)

        # Aggregate sum of coupons, empty bottles, and cash from OutstandingLog
        outstanding_log_aggregates = OutstandingLog.objects.filter(customer=user_det).aggregate(
            total_coupons=Sum('coupons'),
            total_empty_bottles=Sum('empty_bottles'),
            total_cash=Sum('cash')
        )
        # Check if all values in outstanding_log_aggregates are None
        if all(value is None for value in outstanding_log_aggregates.values()):
            outstanding_log_aggregates = None

        # Prepare the product form
        product_form = ProductForm()

        # Remove the coupon_method field from the form if sale type is "CASH" or "CREDIT"
        if sales_type in ["CASH", "CREDIT"]:
            del product_form.fields['coupon_method']
        # Add custody_items and aggregated data to the context
        context = {
            'user_det': user_det,
            'visit_schedule_data': data_for_rendering,
            'custody_items': custody_items,
            'outstanding_log_aggregates': outstanding_log_aggregates,  # Add aggregated data to the context
            'product_form': product_form,  # Add the product form to the context
        }

        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        print("dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd")
        # Retrieve user details
        user_det = Customers.objects.get(customer_id=pk)

        # Process product form submission
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            # Save the product form data
            product = product_form.save(commit=False)
            product.created_by = request.user.username  # Set the created_by field
            product.save()
            return redirect('customer_details', pk=pk)
        else:
            # If the form is not valid, re-render the page with the form errors
            context = {
                'user_det': user_det,
                'product_form': product_form,
                # Add other context data as needed
            }
            return render(request, self.template_name, context)
        
#------------------SALES REPORT-------------------------        

        
def salesreport(request):
    instances = CustomUser.objects.filter(user_type='Salesman')
    print("instances",instances)
    return render(request, 'sales_management/sales_report.html', {'instances': instances})

def salesreportview(request, salesman):
    salesman = get_object_or_404(CustomUser, pk=salesman)
    customer_supplies = CustomerSupply.objects.filter(salesman=salesman)
    customer_supply_items = CustomerSupplyItems.objects.filter(customer_supply__in=customer_supplies)

    # Calculate counts of products for each sales type
    cash_coupon_counts = customer_supplies.filter(customer__sales_type='CASH COUPON').aggregate(total_products=Count('customersupplyitems'))

    # print("cash_coupon_counts",cash_coupon_counts)
    credit_coupon_counts = customer_supplies.filter(customer__sales_type='CREDIT COUPON').aggregate(total_products=Count('customersupplyitems'))
    # print("credit_coupon_counts",credit_coupon_counts)
    cash_counts = customer_supplies.filter(customer__sales_type='CASH').aggregate(total_products=Count('customersupplyitems'))
    # print("cash_counts",cash_counts)
    credit_counts = customer_supplies.filter(customer__sales_type='CREDIT').aggregate(total_products=Count('customersupplyitems'))
    # print("credit_counts",credit_counts)
    
    context = {
        'salesman': salesman,
        'customer_supplies':customer_supplies,
        'customer_supply_items':customer_supply_items,
        'cash_coupon_counts': cash_coupon_counts['total_products'],
        'credit_coupon_counts': credit_coupon_counts['total_products'],
        'cash_counts': cash_counts['total_products'],
        'credit_counts': credit_counts['total_products'],
    }

    return render(request, 'sales_management/salesreportview.html', context)

def download_salesreport_pdf(request):
    # Retrieve sales report data
    customer_supplies = CustomerSupply.objects.all()
    # Check if customer_supplies is not empty
    if customer_supplies:
        # Create the HTTP response with PDF content type and attachment filename
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'

        # Create a PDF document
        pdf_buffer = BytesIO()
        pdf = SimpleDocTemplate(pdf_buffer, pagesize=letter)
        data = []

        # Add headers
        headers = ['Customer Name', 'Customer Address', 'Customer Type', 'Customer Sales Type', 
                   'Cash Coupon Quantity','Credit Coupon Quantity','Cash Quantity','Credit Quantity']
        data.append(headers)


        # Add data to the PDF document
        sl_no = 1
        for supply in customer_supplies:
            try:
                cash_coupon_counts = supply.customersupplyitems_set.filter(customer_supply=supply, customer_supply__customer__sales_type='CASH COUPON').count()
                credit_coupon_counts = supply.customersupplyitems_set.filter(customer_supply=supply, customer_supply__customer__sales_type='CREDIT COUPON').count()
                cash_counts = supply.customersupplyitems_set.filter(customer_supply=supply, customer_supply__customer__sales_type='CASH').count()
                credit_counts = supply.customersupplyitems_set.filter(customer_supply=supply, customer_supply__customer__sales_type='CREDIT').count()
            except Exception as e:
                print(e)
                cash_coupon_counts = 0
                credit_coupon_counts = 0
                cash_counts = 0
                credit_counts = 0
            
            # Append data for each supply
            data.append([
                sl_no,
                supply.customer.customer_name,
                f"{supply.customer.building_name} {supply.customer.door_house_no}",
                supply.customer.customer_type,
                supply.customer.sales_type,
                cash_coupon_counts,
                credit_coupon_counts,
                cash_counts,
                credit_counts
            ])
            sl_no += 1

        table = Table(data)
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)])
        table.setStyle(style)

        # Add the table to the PDF document
        elements = [table]
        pdf.build(elements)

        # Get the value of the BytesIO buffer and write it to the response
        pdf_value = pdf_buffer.getvalue()
        pdf_buffer.close()
        response.write(pdf_value)

        return response
    else:
        return HttpResponse("No data available for sales report.")
    

def download_salesreport_excel(request):
    # Create a new Excel workbook
    workbook = Workbook()
    worksheet = workbook.active

    # Add headers to the worksheet
    headers = ['Sl No', 'Customer Name', 'Customer Address', 'Customer Type', 
               'Customer Sales Type', 'Cash Coupon Quantity', 'Credit Coupon Quantity', 
               'Cash Quantity', 'Credit Quantity']
    worksheet.append(headers)

    # Retrieve sales report data
    customer_supplies = CustomerSupply.objects.all()

    # Add data to the worksheet
    sl_no = 1
    for supply in customer_supplies:
        try:
            
            cash_coupon_counts = supply.customersupplyitems_set.filter(customer_supply=supply, customer_supply__customer__sales_type='CASH COUPON').count()
            print("cash_coupon_counts",cash_coupon_counts)
            credit_coupon_counts = supply.customersupplyitems_set.filter(customer_supply=supply, customer_supply__customer__sales_type='CREDIT COUPON').count()
            print("credit_coupon_counts",credit_coupon_counts)
            cash_counts = supply.customersupplyitems_set.filter(customer_supply=supply, customer_supply__customer__sales_type='CASH').count()
            print("cash_counts",cash_counts)
            credit_counts = supply.customersupplyitems_set.filter(customer_supply=supply, customer_supply__customer__sales_type='CREDIT').count()
            print("credit_counts",credit_counts)

        except Exception as e:
            print(e)
            cash_coupon_counts = 0
            credit_coupon_counts = 0
            cash_counts = 0
            credit_counts = 0
        
        # Write data for each supply to the worksheet
        row_data = [
            sl_no,
            supply.customer.customer_name,
            f"{supply.customer.building_name} {supply.customer.door_house_no}",
            supply.customer.customer_type,
            supply.customer.sales_type,
            cash_coupon_counts,
            credit_coupon_counts,
            cash_counts,
            credit_counts
        ]
        worksheet.append(row_data)

        sl_no += 1

    # Create HTTP response with Excel content type and attachment filename
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="sales_report.xlsx"'

    # Write the workbook data into the response
    workbook.save(response)

    # Write headers
    headers = ['Customer Name', 'Customer Address', 'Product', 'Quantity', 'Amount']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    # Write data to the Excel workbook
    row = 1  # Start from row 1 since row 0 is for headers
    for supply in customer_supplies:
        for item in supply.customersupplyitems_set.all():
            customer_address = ", ".join(filter(None, [supply.customer.building_name, supply.customer.door_house_no, supply.customer.floor_no]))
            product_name = "Product Not Found"
            if item.product:  # Check if product is not None
                product_name = item.product.product_name
            worksheet.write(row, 0, supply.customer.customer_name)
            worksheet.write(row, 1, customer_address)
            worksheet.write(row, 2, product_name)
            worksheet.write(row, 3, item.quantity)
            worksheet.write(row, 4, item.amount)
            row += 1

    workbook.close()

    return response

#------------------Collection Report-------------------------                
def collectionreport(request):
    start_date = None
    end_date = None
    selected_date = None
    selected_route_id = None
    selected_route = None
    template = 'sales_management/collection_report.html'
    colectionpayment = CollectionPayment.objects.all()
    
    routes = RouteMaster.objects.all()
    route_counts = {}
    today = datetime.today()
    
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        selected_date = request.POST.get('date')
        selected_route_id = request.POST.get('selected_route_id')
        if start_date and end_date:
            colectionpayment = colectionpayment.filter(customer_supply__created_date__range=[start_date, end_date])
        elif selected_date:
            colectionpayment = colectionpayment.filter(customer_supply__created_date=selected_date)
        
        if selected_route_id:
            selected_route = RouteMaster.objects.get(id=selected_route_id)
            colectionpayment = colectionpayment.filter(customer__routes__route_name=selected_route)
    
    # /
    
    context = {
        'colectionpayment': colectionpayment, 
        'routes': routes, 
        'route_counts': route_counts, 
        'today': today,
        'start_date': start_date, 
        'end_date': end_date, 
        'selected_date': selected_date, 
        'selected_route_id': selected_route_id, 
        'selected_route': selected_route,
        
    }
    return render(request, template, context)



def collection_report_excel(request):
    instances = CollectionPayment.objects.all()
    route_filter = request.GET.get('route_name')
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    
    if start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        instances = instances.filter(customer__customer_supply__created_date__range=[start_date, end_date])
    
    print('route_filter :', route_filter)
    if route_filter and route_filter != '' and route_filter != 'None':
        instances = instances.filter(routes__route_name=route_filter)

    route_li = RouteMaster.objects.all()
    serial_number = 1
    for customer in instances:
        customer.serial_number = serial_number
        serial_number += 1
    data = {
        'Serial Number': [customer.serial_number for customer in instances],
        'Date': [customer.customer_supply.created_date.date() for customer in instances],
        'Customer name': [customer.customer.customer_name for customer in instances],
        'Mobile No': [customer.customer.mobile_no for customer in instances],
        'Route': [customer.customer.routes.route_name if customer.customer.routes else '' for customer in instances],
        'Building Name': [customer.customer.building_name for customer in instances],
        'House No': [customer.customer.door_house_no if customer.customer.door_house_no else 'Nil' for customer in instances],
        'Receipt No/Reference No': [customer.customer_supply.reference_number for customer in instances],
        'Amount': [customer.amount for customer in instances],
        'Mode of Payment': [customer.payment_method for customer in instances],

    }
    df = pd.DataFrame(data)

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False, startrow=4)
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        table_border_format = workbook.add_format({'border':1})
        worksheet.conditional_format(4, 0, len(df.index)+4, len(df.columns) - 1, {'type':'cell', 'criteria': '>', 'value':0, 'format':table_border_format})
        merge_format = workbook.add_format({'align': 'center', 'bold': True, 'font_size': 16, 'border': 1})
        worksheet.merge_range('A1:J2', f'National Water', merge_format)
        merge_format = workbook.add_format({'align': 'center', 'bold': True, 'border': 1})
        worksheet.merge_range('A3:J3', f'    Collection Report   ', merge_format)
        merge_format = workbook.add_format({'align': 'center', 'bold': True, 'border': 1})
        worksheet.merge_range('A4:J4', '', merge_format)
    
    filename = f"Collection Report.xlsx"
    response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'inline; filename = "{filename}"'
    return response


def dailycollectionreport(request):
    instances = CollectionPayment.objects.all()
    route_filter = request.GET.get('route_name')
    start_date_str = request.GET.get('start_date')

    if start_date_str :
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        instances = instances.filter(created_date__range=start_date)
    if route_filter:
            instances = instances.filter(routes__route_name=route_filter)
    route_li = RouteMaster.objects.all()
    
    context = {'instances': instances,'route_li':route_li}
    return render(request, 'sales_management/daily_collection_report.html', context)


def daily_collection_report_excel(request):
    instances = CollectionPayment.objects.all()
    route_filter = request.GET.get('route_name')
    start_date_str = request.GET.get('start_date')
    
    if start_date_str :
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        instances = instances.filter(customer__customer_supply__created_date__range=start_date)
    
    print('route_filter :', route_filter)
    if route_filter and route_filter != '' and route_filter != 'None':
        instances = instances.filter(routes__route_name=route_filter)

    route_li = RouteMaster.objects.all()
    serial_number = 1
    for customer in instances:
        customer.serial_number = serial_number
        serial_number += 1
    data = {
        'Serial Number': [customer.serial_number for customer in instances],
        'Customer name': [customer.customer.customer_name for customer in instances],
        'Mobile No': [customer.customer.mobile_no for customer in instances],
        'Route': [customer.customer.routes.route_name if customer.customer.routes else '' for customer in instances],
        'Building Name': [customer.customer.building_name for customer in instances],
        'House No': [customer.customer.door_house_no if customer.customer.door_house_no else 'Nil' for customer in instances],
        'Receipt No/Reference No': [customer.customer_supply.reference_number for customer in instances],
        'Amount': [customer.amount for customer in instances],
        'Mode of Payment': [customer.payment_method for customer in instances],
        'Invoice': [customer.invoice.invoice_no for customer in instances],
        'Invoice Reference No': [customer.invoice.reference_no  for customer in instances],


    }
    df = pd.DataFrame(data)

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False, startrow=4)
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        table_border_format = workbook.add_format({'border':1})
        worksheet.conditional_format(4, 0, len(df.index)+4, len(df.columns) - 1, {'type':'cell', 'criteria': '>', 'value':0, 'format':table_border_format})
        merge_format = workbook.add_format({'align': 'center', 'bold': True, 'font_size': 16, 'border': 1})
        worksheet.merge_range('A1:J2', f'National Water', merge_format)
        merge_format = workbook.add_format({'align': 'center', 'bold': True, 'border': 1})
        worksheet.merge_range('A3:J3', f'    Daily Collection Report   ', merge_format)
        # worksheet.merge_range('E3:H3', f'Date: {def_date}', merge_format)
        # worksheet.merge_range('I3:M3', f'Total bottle: {total_bottle}', merge_format)
        merge_format = workbook.add_format({'align': 'center', 'bold': True, 'border': 1})
        worksheet.merge_range('A4:J4', '', merge_format)
    
    filename = f"Daily Collection Report.xlsx" 
    response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'inline; filename = "{filename}"'
    return response

#------------------Product-Route wise sales report


def product_route_salesreport(request):
    start_date = None
    end_date = None
    selected_date = None
    selected_product_id = None
    selected_product = None
    template = 'sales_management/product_route_salesreport.html'
    customersupplyitems = CustomerSupplyItems.objects.all()
    # print("customersupplyitems",customersupplyitems)
    products = ProdutItemMaster.objects.all()
    route_counts = {}
    today = datetime.today()
    
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        # print("start_date",start_date)
        end_date = request.POST.get('end_date')
        # print("end_date",end_date)
        selected_date = request.POST.get('date')
        selected_product_id = request.POST.get('selected_product_id')
        # print("selected_product_id",selected_product_id)
        if start_date and end_date:
            customersupplyitems = customersupplyitems.filter(customer_supply__created_date__range=[start_date, end_date])
        elif selected_date:
            customersupplyitems = customersupplyitems.filter(customer_supply__created_date=selected_date)
        else:
            customersupplyitems = CustomerSupplyItems.objects.filter(customer_supply__created_date=timezone.now().date())
        # print("customersupplyitemsHHHHHHHHHHHHHHHHHHHH",customersupplyitems)
        
        if selected_product_id:
            selected_product = ProdutItemMaster.objects.get(id=selected_product_id)
            customersupplyitems = customersupplyitems.filter(product=selected_product)
    
    else:
        customersupplyitems = CustomerSupplyItems.objects.filter(customer_supply__created_date=timezone.now().date())
    
    total_quantity = customersupplyitems.aggregate(total_quantity=Sum('quantity'))['total_quantity']
    print("total_quantity",total_quantity)
    total_amount = customersupplyitems.aggregate(total_amount=Sum('amount'))['total_amount']
    print("total_amount",total_amount)
    context = {
        'customersupplyitems': customersupplyitems, 
        'products': products, 
        'route_counts': route_counts, 
        'today': today,
        'start_date': start_date, 
        'end_date': end_date, 
        'selected_date': selected_date, 
        'selected_product_id': selected_product_id, 
        'selected_product': selected_product,
        'total_quantity': total_quantity,
        'total_amount': total_amount,
    }
    return render(request, template, context)

def product_route_salesreport_detail_view(request, customersupplyitem_id):
    customersupplyitem = get_object_or_404(CustomerSupplyItems, id=customersupplyitem_id)
    return render(request, 'sales_management/product_route_salesreport_detail.html', {'customersupplyitem': customersupplyitem}) 

def print_product_sales(request):
    # Retrieve sales report data
    customer_supplies = CustomerSupplyItems.objects.all()
    # Check if customer_supplies is not empty
    if customer_supplies:
        # Create the HTTP response with PDF content type and attachment filename
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'

        # Create a PDF document
        pdf_buffer = BytesIO()
        pdf = SimpleDocTemplate(pdf_buffer, pagesize=letter)
        data = []

        # Add headers
        headers = ['Sl No', 'Salesman', 'Customer Name', 'Product', 'Quantity', 'Amount']
        data.append(headers)

        total_quantity = 0
        total_amount = 0

        # Add data to the PDF document
        sl_no = 1
        for supply in customer_supplies:
            # Append data for each supply
            data.append([
                sl_no,
                supply.customer_supply.salesman.username,
                supply.customer_supply.customer.customer_name,
                supply.product,
                supply.quantity,
                supply.amount,
            ])
            # Update total quantity and amount
            total_quantity += supply.quantity
            total_amount += supply.amount
            sl_no += 1

        # Add footer with total quantity and amount
        footer = ['Total', '', '', '', total_quantity, total_amount]
        data.append(footer)

        table = Table(data)
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)])
        table.setStyle(style)

        # Add the table to the PDF document
        elements = [table]
        pdf.build(elements)

        # Get the value of the BytesIO buffer and write it to the response
        pdf_value = pdf_buffer.getvalue()
        pdf_buffer.close()
        response.write(pdf_value)

        return response
    else:
        return HttpResponse("No data available for sales report.")

def download_product_sales_excel(request):
    # Retrieve sales report data
    customer_supplies = CustomerSupplyItems.objects.all()

    # Create the HttpResponse object with Excel content type and attachment filename
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="sales_report.xlsx"'

    # Create a new Excel workbook and add a worksheet
    workbook = xlsxwriter.Workbook(response)
    worksheet = workbook.add_worksheet()

    # Define cell formats
    bold_format = workbook.add_format({'bold': True})

    # Write headers
    headers = ['Sl No', 'Salesman', 'Customer Name', 'Product', 'Quantity', 'Amount']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, bold_format)

    # Write data rows
    for row, supply in enumerate(customer_supplies, start=1):
        worksheet.write(row, 0, row)  # Sl No
        worksheet.write(row, 1, supply.customer_supply.salesman.username)  # Salesman
        worksheet.write(row, 2, supply.customer_supply.customer.customer_name)  # Customer Name
        worksheet.write(row, 3, supply.product.product_name)  # Product
        worksheet.write(row, 4, supply.quantity)  # Quantity
        worksheet.write(row, 5, supply.amount)  # Amount

    # Calculate and write total quantity and amount
    total_quantity = sum(supply.quantity for supply in customer_supplies)
    total_amount = sum(supply.amount for supply in customer_supplies)
    worksheet.write(len(customer_supplies) + 1, 4, total_quantity, bold_format)  # Total Quantity
    worksheet.write(len(customer_supplies) + 1, 5, total_amount, bold_format)  # Total Amount

    # Close the workbook
    workbook.close()

    return response


# def yearmonthsalesreport(request):
#     user_li = Customers.objects.all()
#     # user_li = user_li.filter(routes__route_name=route_filter)
#     route_li = RouteMaster.objects.all()

#     context = {
#         'user_li': user_li, 
#         'route_li': route_li,
        
#             }
#     # route_li = RouteMaster.objects.all()
#     # print(route_li,'route_li')
#     # context = {'route_li': route_li}

#     return render(request,'sales_management/yearmonthsalesreport.html',context)
def yearmonthsalesreport(request):
    # Get all customers and routes
    user_li = Customers.objects.all()
    route_li = RouteMaster.objects.all()

    # Calculate YTD and MTD sales for each route
    route_sales = []
    current_year = datetime.now().year
    print(route_sales,"route_sales")
    print(current_year,'current_year')
    current_month = datetime.now().month
    print(current_month,'current_month')


    for route in route_li:
        ytd_sales = CustomerSupply.objects.filter(customer__routes=route, created_date__year=current_year).aggregate(total_sales=Sum('grand_total'))['total_sales'] or 0
        print('ytd_sales',ytd_sales)

        mtd_sales = CustomerSupply.objects.filter(customer__routes=route, created_date__year=current_year, created_date__month=current_month).aggregate(total_sales=Sum('grand_total'))['total_sales'] or 0
        print('mtd_sales',mtd_sales)

        route_sales.append({
            'route': route,
            'ytd_sales': ytd_sales,
            'mtd_sales': mtd_sales,
            'year': current_year,
        })
        print(route_sales,'route_sales')


    context = {
        'user_li': user_li, 
        'route_li' : route_li,
        'route_sales': route_sales,
    }

    return render(request, 'sales_management/yearmonthsalesreport.html', context)

# def yearmonthsalesreportview(request,route_id):
#     route = RouteMaster.objects.get(route_id = route_id)
#     print(route,'route')
#     route_customer = Customers.objects.filter(routes__route_name=route)
#     print(route_customer,'route_customer')

#     context = {
#         'route_customer': route_customer
#         }
    
#     return render(request, 'sales_management/yearmonthsalesreportview.html',context)
# def yearmonthsalesreportview(request, route_id):
#     route = RouteMaster.objects.get(route_id=route_id)
#     route_customers = Customers.objects.filter(routes__route_name=route)

#     # Calculate YTD and MTD sales for each customer
#     today = date.today()
#     ytd_sales = CustomerSupply.objects.filter(customer__in=route_customers, created_date__year=today.year).aggregate(total_ytd_sales=Sum('grand_total'))['total_ytd_sales'] or 0
#     mtd_sales = CustomerSupply.objects.filter(customer__in=route_customers, created_date__year=today.year, created_date__month=today.month).aggregate(total_mtd_sales=Sum('grand_total'))['total_mtd_sales'] or 0

#     # Associate YTD and MTD sales with each customer
#     customers_with_sales = []
#     for customer in route_customers:
#         ytd_customer_sales = CustomerSupply.objects.filter(customer=customer, created_date__year=today.year).aggregate(total_ytd_sales=Sum('grand_total'))['total_ytd_sales'] or 0
#         mtd_customer_sales = CustomerSupply.objects.filter(customer=customer, created_date__year=today.year, created_date__month=today.month).aggregate(total_mtd_sales=Sum('grand_total'))['total_mtd_sales'] or 0

#         customers_with_sales.append({
#             'customer': customer,
#             'ytd_sales': ytd_customer_sales,
#             'mtd_sales': mtd_customer_sales
#         })

#     context = {
#         'route': route,
#         'customers_with_sales': customers_with_sales,
#         'ytd_sales': ytd_sales,
#         'mtd_sales': mtd_sales
#     }

#     return render(request, 'sales_management/yearmonthsalesreportview.html', context)

from datetime import datetime
def yearmonthsalesreportview(request, route_id):
    route = RouteMaster.objects.get(route_id=route_id)
    current_year = datetime.now().year

    yearly_sales = CustomerSupply.objects.filter(customer__routes=route, created_date__year=current_year).aggregate(total_sales=Sum('grand_total'))['total_sales'] or 0

    customers = Customers.objects.filter(routes__route_name=route)
    monthly_sales = []
    for customer in customers:
        monthly_sales_data = []
        for month in range(1, 13):
            month_date = datetime(current_year, month, 1)

            month_name = month_date.strftime("%B")  # Get month name
            monthly_sales_amount = CustomerSupply.objects.filter(customer=customer, created_date__year=current_year, created_date__month=month).aggregate(total_sales=Sum('grand_total'))['total_sales'] or 0
            monthly_sales_data.append({month_name: monthly_sales_amount})  # Append month name and sales amount
        monthly_sales.append({'customer': customer, 'monthly_sales': monthly_sales_data})

    context = {
        'route_id': route_id,
        'yearly_sales': yearly_sales,
        'monthly_sales': monthly_sales,
    }
    return render(request, 'sales_management/yearmonthsalesreportview.html', context)
