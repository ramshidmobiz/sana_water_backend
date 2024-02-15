from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('products', Products_List.as_view(), name='products'),
    path('product_create',Product_Create.as_view(), name='product_create'),
    path('product_edit/<str:pk>', Product_Edit.as_view(), name='product_edit'),
    path('product_details/<str:pk>', Product_Details.as_view(), name='product_details'),
    path('product_delete/<str:pk>', ProductDelete.as_view(), name='product_delete'),

    path('defaultprice', Defaultprice_List.as_view(), name='defaultprice'),
    path('defaultprice_create', Defaultprice_Create.as_view(), name='defaultprice_create'),
    path('defaultprice_edit/<str:pk>', Defaultprice_Edit.as_view(), name='defaultprice_edit'),
    path('defaultprice_delete/<str:product_name>', Defaultprice_Delete.as_view(), name='defaultprice_delete'),
    
    
    # path('staff_issue_orders_list/', StaffIssueOrdersList.as_view(), name='staff_issue_orders_list'),

    path('staff_issue_orders_list/',staffIssueOrdersList, name='staff_issue_orders_list'),
    path('staffIssueOrdersCreate/<str:staff_order_details_id>/',staffIssueOrdersCreate, name='staffIssueOrdersCreate'),

   ]

    # path('staff_issue_orders_create/<str:staff_order_details_id>', StaffIssueOrdersCreate.as_view(), name='staff_issue_orders_create'),
