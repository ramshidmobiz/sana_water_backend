from django.urls import path,re_path

from . import views
from . views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('get-coupon-bookno/', get_coupon_bookno, name='get_coupon_bookno'),
    path('get-product-items/', get_product_items, name='get_product_items'),
    
    path('products', Products_List.as_view(), name='products'),
    path('product_create',Product_Create.as_view(), name='product_create'),
    path('product_edit/<str:pk>', Product_Edit.as_view(), name='product_edit'),
    path('product_details/<str:pk>', Product_Details.as_view(), name='product_details'),
    path('product_delete/<str:pk>', ProductDelete.as_view(), name='product_delete'),

    path('defaultprice', Defaultprice_List.as_view(), name='defaultprice'),
    path('defaultprice_create', Defaultprice_Create.as_view(), name='defaultprice_create'),
    path('defaultprice_edit/<str:pk>', Defaultprice_Edit.as_view(), name='defaultprice_edit'),
    path('defaultprice_delete/<str:product_name>', Defaultprice_Delete.as_view(), name='defaultprice_delete'),
    
    path('staff-issue-orders-list',staff_issue_orders_list, name='staff_issue_orders_list'),
    path('staff-issue-order-details/<str:staff_order_id>/', staff_issue_orders_details_list, name='staff_issue_orders_details_list'),
    
    path('staffIssueOrdersCreate/<str:staff_order_details_id>/',staffIssueOrdersCreate, name='staffIssueOrdersCreate'),
    path('issue_coupons_orders/', issue_coupons_orders, name='issue_coupons_orders'),
    # path('coupon_issue_orders_create/',couponIssueOrdersList, name='coupon_issue_orders_create'),
    path('product_items', Product_items_List.as_view(), name='product_items'),
    path('product_items_create',Product_items_Create.as_view(), name='product_items_create'),
    path('product_item_edit/<str:pk>',Product_Item_Edit.as_view(), name='product_item_edit'),
    # path('product_item_delete/<str:pk>/',delete_product_item, name='product_item_delete'),
    re_path(r'^product_item_delete/(?P<pk>.*)/$', views.delete_product_item, name='delete_product_item'),

    path('product_stock_report', product_stock_report, name='product_stock_report'),
    path('download_productstock_pdf', download_productstock_pdf, name='download_productstock_pdf'),
    path('product_stock_excel_download', product_stock_excel_download, name='product_stock_excel_download'),
    path('stocktransfer/', stock_transfer_view, name='stocktransfer'),
    path('scrap_stock_transfer_view/', scrap_stock_transfer_view, name='scrap_stock_transfer_view'),


   ]

