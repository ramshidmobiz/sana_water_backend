from django.urls import path

from sales_management.views import *

urlpatterns = [
    path('sale_entry_log_view/', SaleEntryLogView.as_view(), name='sale_entry_log_view'),
    path('customer_details_view/<str:pk>',CustomerDetailsView.as_view(), name='customer_details_view'),
    path('get_products_by_category/', GetProductsByCategoryView.as_view(), name='get_products_by_category'),
    path('initiate_sale/', InitiateSaleView.as_view(), name='initiate_sale'),
    path('payment_form/', PaymentForm.as_view(), name='payment_form'),
    path('collectamount/', CalculateTotaltoCollect.as_view(), name='collectamount'),


    path('sale_entry_log_list/', SaleEntryLogListView.as_view(), name='sale_entry_log_list'),
    path('transaction_history_list/', TransactionHistoryListView.as_view(), name='transaction_history_list'),
    path('outstanding_log_list/', OutstandingLogListView.as_view(), name='outstanding_log_list'),
    path('payment_submit/', payment_submit, name='payment_submit'),

    

    path('coupon_sale', CouponSaleView.as_view(), name='coupon_sale'),
    path('details_view/<str:pk>',DetailsView.as_view(), name='details_view'),

#--------------Sales Report---------------------------------
   path('salesreport', salesreport, name='salesreport'),
    path('salesreportview/<int:salesman>/', salesreportview, name='salesreportview'),
    path('download-salesreport-pdf/', download_salesreport_pdf, name='download_salesreport_pdf'),
    path('download-salesreport-excel/', download_salesreport_excel, name='download_salesreport_excel'),

    
    path('collectionreport', collectionreport, name='collectionreport'),
    
    # path('create-sale/', SaleEntryCreateView.as_view(), name='create_sale'),
    # path('create-sales-entry/', SalesEntryCreateView.as_view(), name='initiate_sale'),


    
    




]