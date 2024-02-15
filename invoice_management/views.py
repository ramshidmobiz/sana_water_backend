import json
import random
import datetime
# django
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.forms import inlineformset_factory
from django.contrib.auth.models import User,Group
from django.forms.formsets import formset_factory
from django.db import transaction, IntegrityError
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from product.models import Product, Product_Default_Price_Level

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view,renderer_classes, permission_classes
#local
from invoice_management.models import Invoice, InvoiceItems
from invoice_management.serializers import BuildingNameSerializers, ProductSerializers,CustomersSerializers
from master.functions import generate_form_errors
from master.models import CategoryMaster, RouteMaster
from accounts.models import Customers
from invoice_management.forms import InvoiceForm, InvoiceItemsForm

# Create your views here.
@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def get_building_no(request,route_id):
    customers = Customers.objects.filter(routes__pk=route_id)
    serialized = BuildingNameSerializers(customers, many=True, context={"request":request})

    response_data = {
        "StatusCode" : 6000,
        "data" : serialized.data,
    }
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def get_customer(request,route_id,building_no):
    customers = Customers.objects.filter(routes__pk=route_id,building_name=building_no)
    serialized = CustomersSerializers(customers, many=True, context={"request":request})

    response_data = {
        "StatusCode" : 6000,
        "data" : serialized.data,
    }
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def get_products(request,category_id):
    category = Product.objects.filter(category_id__pk=category_id)
    serialized = ProductSerializers(category, many=True, context={"request":request})

    response_data = {
        "StatusCode" : 6000,
        "data" : serialized.data,
    }
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def get_customer_rate(request,product,customer):
    product_price = 0
    vat_rate = 0
    total_include_vat = 0
    # print(product)
    # print(customer)
    try :
        product = Product.objects.get(pk=product)
        customer = Customers.objects.get(pk=customer)
        product_price = Product_Default_Price_Level.objects.get(product_id=product,customer_type=customer.customer_type).rate
        
        if product.tax:
            # print('vat')
            vat_rate = product.tax.percentage
            # print(vat_rate)
            total_include_vat = (float(vat_rate)/100) * float(product_price)
            # print(total_include_vat, "vat")
        
        
        response_data = {
            "StatusCode" : 6000,
            'product_price':product_price,
            'total_include_vat':total_include_vat,
        }
    except:
        response_data = {
            "StatusCode" : 6001,
            'product_price':product_price,
            'total_include_vat':total_include_vat,
        }
    return Response(response_data, status=status.HTTP_200_OK)

@login_required
def invoice_info(request,pk):
    """
    single view of invoice
    :param request:
    :return: invoice single view
    """
    instance = Invoice.objects.get(pk=pk,is_deleted=False)
    
    context = {
        'instance': instance,
        'page_name' : 'Invoice',
        'page_title' : 'Invoice',
        'is_invoice': True,
    }

    return render(request, 'invoice_management/info.html', context)

@login_required
def invoice_list(request):
    """
    Invoice List
    :param request:
    :return: Invoices list view
    """
    
    instances = Invoice.objects.filter(is_deleted=False).order_by("-created_date")
         
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
            Q(invoice_no__icontains=query) |
            Q(product__invoice_id__icontains=query) 
        )
        title = "Invoice List - %s" % query
        filter_data['q'] = query
    
    context = {
        'instances': instances,
        'page_name' : 'Invoice List',
        'page_title' : 'Invoice List',
        'filter_data' :filter_data,
        'date_range': date_range,
        
        'is_invoice': True,
        'is_need_datetime_picker': True,
    }

    return render(request, 'invoice_management/list.html', context)

@login_required
def create_invoice(request):
    InvoiceItemsFormset = formset_factory(InvoiceItemsForm, extra=2)
    
    message = ''
    if request.method == 'POST':
        invoice_form = InvoiceForm(request.POST)
        invoice_items_formset = InvoiceItemsFormset(request.POST,prefix='invoice_items_formset', form_kwargs={'empty_permitted': False})
        
        if invoice_form.is_valid() and invoice_items_formset.is_valid():
            
            date_part = timezone.now().strftime('%Y%m%d')
            random_part = str(random.randint(1000, 9999))
            invoice_number = f'WTR-{date_part}-{random_part}'
            
            # try:
            #     with transaction.atomic():
            customer_instance = Customers.objects.get(pk=invoice_form.cleaned_data['customer_id'])
            
            invoice = invoice_form.save(commit=False)
            invoice.created_date = datetime.datetime.today()
            invoice.invoice_no = invoice_number
            invoice.customer = customer_instance
            invoice.save()
            
            for form in invoice_items_formset:
                data = form.save(commit=False)
                data.invoice = invoice
                data.save()
            
            response_data = {
                "status": "true",
                "title": "Successfully Created",
                "message": "Invoice created successfully.",
                'redirect': 'true',
                "redirect_url": reverse('invoice:invoice_list')
            }
                    
            # except IntegrityError as e:
            #     # Handle database integrity error
            #     response_data = {
            #         "status": "false",
            #         "title": "Failed",
            #         "message": "Integrity error occurred. Please check your data.",
            #     }

            # except Exception as e:
            #     # Handle other exceptions
            #     response_data = {
            #         "status": "false",
            #         "title": "Failed",
            #         "message": str(e),
            #     }
        else:
            message = generate_form_errors(invoice_form,formset=False)
            message += generate_form_errors(invoice_items_formset,formset=True)
            
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    
    else:
        invoice_form = InvoiceForm()
        invoice_items_formset = InvoiceItemsFormset(prefix='invoice_items_formset')
        route_instances = RouteMaster.objects.all()
        
        context = {
            'invoice_form': invoice_form,
            'invoice_items_formset': invoice_items_formset,
            'route_instances' : route_instances,
            
            'page_title': 'Create invoice',
            'url': reverse('invoice:create_invoice'),
            'invoice_page': True,
            'is_need_datetime_picker': True
        }
        
        return render(request,'invoice_management/create.html',context)

@login_required
def edit_invoice(request,pk):
    """
    edit operation of invoice
    :param request:
    :param pk:
    :return:
    """
    invoice_instance = get_object_or_404(Invoice, pk=pk)
    invoice_items = InvoiceItems.objects.filter(invoice=invoice_instance)
    
    if invoice_items.exists():
        extra = 0
    else:
        extra = 1 

    InvoiceItemsFormset = inlineformset_factory(
        Invoice,
        InvoiceItems,
        extra=extra,
        form=InvoiceItemsForm,
    )
        
    message = ''
    
    if request.method == 'POST':
        invoice_form = InvoiceForm(request.POST,instance=invoice_instance)
        invoice_items_formset = InvoiceItemsFormset(request.POST,request.FILES,
                                            instance=invoice_instance,
                                            prefix='invoice_items_formset',
                                            form_kwargs={'empty_permitted': False})            
        
        if invoice_form.is_valid() and  invoice_items_formset.is_valid() :
            #create
            data = invoice_form.save(commit=False)
            data.save()
            
            for form in invoice_items_formset:
                if form not in invoice_items_formset.deleted_forms:
                    i_data = form.save(commit=False)
                    if not i_data.invoice :
                        i_data.invoice = invoice_instance
                    i_data.save()

            for f in invoice_items_formset.deleted_forms:
                f.instance.delete()
                
            response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "invoice Updated Successfully.",
                'redirect': 'true',
                "redirect_url": reverse('invoice:invoice_list'),
                "return" : True,
            }
    
        else:
            message = generate_form_errors(invoice_form,formset=False)
            message += generate_form_errors(invoice_items_formset,formset=True)
            
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
                        
    else:
        # initial_values = []
        # for invoice_item in invoice_items:
        #     category_id = invoice_item.product.category_id
        #     initial_values.append({'category': category_id})

        invoice_form = InvoiceForm(instance=invoice_instance,initial={'customer_id': invoice_instance.customer.pk})
        invoice_items_formset = InvoiceItemsFormset(queryset=invoice_items,
                                                    prefix='invoice_items_formset',
                                                    instance=invoice_instance)
        # category_ids = [invoice_item.product.category_id for invoice_item in invoice_items]

        # # Create a list of initial data for each form in the formset
        # initial_data = [{'category': category_id} for category_id in category_ids]

        # # Create the formset instance with initial data
        # invoice_items_formset = InvoiceItemsFormset(
        #     queryset=invoice_items,
        #     prefix='invoice_items_formset',
        #     instance=invoice_instance,
        #     initial=initial_data
        # )
                
        route_instances = RouteMaster.objects.all()
        building_names_queryset = Customers.objects.filter(routes=invoice_form.instance.customer.routes).values_list('building_name', flat=True).distinct()
        # building_names = [name for name in building_names_queryset if isinstance(name, str) and name.strip()]
        

        context = {
            'invoice_form': invoice_form,
            'invoice_items_formset': invoice_items_formset,
            'route_instances': route_instances,
            'building_names': building_names_queryset,
            
            'message': message,
            'page_name' : 'edit invoice',
            'url' : reverse('invoice:edit_invoice', args=[invoice_instance.pk]),
            'invoice_page': True,   
            'is_edit' : True,        
        }

        return render(request, 'invoice_management/create.html', context)
    
@login_required
def delete_invoice(request, pk):
    """
    invoice deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    invoice = Invoice.objects.get(pk=pk)
    invoice.is_deleted=True
    invoice.save()
        
    InvoiceItems.objects.filter(invoice=invoice).update(is_deleted=True)
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "invoice Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('invoice:invoice_list'),
    }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')