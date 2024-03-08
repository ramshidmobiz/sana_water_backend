from django.urls import path
from .views import *
from django.urls import reverse

from django.urls import path,re_path
from . views import *

urlpatterns = [
        path('customer_custody_item/<str:customer_id>', customer_custody_item, name='customer_custody_item'),
        path('get_custody_items', get_custody_items, name='get_custody_items'),


        #vacation
        path('vacation_list', vacation_list, name="vacation_list"),
        path('vacation_add', Vacation_Add.as_view(), name="vacation_add"),
        path('vacation_edit/<uuid:vacation_id>', Vacation_Edit.as_view(), name='vacation_edit'),
        path('vacation_delete/<uuid:vacation_id>',  Vacation_Delete.as_view(), name="vacation_delete"),
        path('vacation_route',  RouteSelection.as_view(), name="vacation_route"),   

        # path('get_route/', get_route.as_view(), name='get_route'),
        # path('get_routes/', GetRoutesView.as_view(), name='get_route'),

        
        # path('create_custody_item/<uuid:pk>', CreateCustodyItemView.as_view(), name='create_custody_item'),

        path('custodyitem_list', Custody_ItemListView.as_view(), name='custodyitem_list'),
        # path('create_custodyitem', CreateCustodyItemView.as_view(), name='create_custodyitem'),

        # path('add_product<str:pk>', Add_ProductView.as_view(), name='add_category_list'),
        # path('get_products_by_category/', GetProductsByCategoryView.as_view(), name='get_products_by_category'),
        # path('get_rate_by_products/', GetRateByProductsView.as_view(), name='get_rate_by_products'),
        # path('added_list', AddListView.as_view(), name='added_list'),
        # path('pullout_list<str:pk>', PulloutListView.as_view(), name='pullout_list'),
        
        re_path(r'customer-supply-list/$', customer_supply_list, name='customer_supply_list'),
        re_path(r'supply-customers/$', customer_supply_customers, name='customer_supply_customers'),
        re_path(r'create-customer-suppply/$', create_customer_supply, name='create_customer_supply'),
        re_path(r'^edit-customer-suppply/(?P<pk>.*)/$', edit_customer_supply, name='edit_customer_supply'),
        re_path(r'^delete-customer-suppply/(?P<pk>.*)/$', delete_customer_supply, name='delete_customer_supply'),

#------------------------------Report-------------------------

        path('client_report', client_report, name='client_report'),
        path('clientdownload_pdf/<uuid:customer_id>/', clientdownload_pdf, name='clientdownload_pdf'),
        path('clientexport_to_csv/<uuid:customer_id>/', clientexport_to_csv, name='clientexport_to_csv'),

        # path('sale_entry_log_view/', SaleEntryLogView.as_view(), name='sale_entry_log_view'),




   
]