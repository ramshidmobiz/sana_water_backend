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
    # path('dailycollectionreport', dailycollectionreport, name='dailycollectionreport'),
    path('collection_report_excel/', collection_report_excel, name='collection_report_excel'),
    # path('daily_collection_report_excel/', daily_collection_report_excel, name='daily_collection_report_excel'),

    # path('create-sale/', SaleEntryCreateView.as_view(), name='create_sale'),
    # path('create-sales-entry/', SalesEntryCreateView.as_view(), name='initiate_sale'),
    
#------------------Product-Route wise sales report

    path('product_route_salesreport', product_route_salesreport, name='product_route_salesreport'),
    path('download_product_sales_excel/', download_product_sales_excel, name='download_product_sales_excel'),
    path('download_product_sales_print/', download_product_sales_print, name='download_product_sales_print'),
   
    #ytd,mtd report
    # ----------------
    path('yearmonthsalesreport', yearmonthsalesreport, name='yearmonthsalesreport'),
    path('yearmonthsalesreportview/<uuid:route_id>/', yearmonthsalesreportview, name="yearmonthsalesreportview"),


    path('customerSales_report',customerSales_report, name='customerSales_report'),
    path('customerSales_Detail_report/<uuid:id>/', customerSales_Detail_report, name='customerSales_Detail_report'),
    path('customerSales_Excel_report',customerSales_Excel_report, name='customerSales_Excel_report'),
    path('customerSales_Print_report',customerSales_Print_report, name='customerSales_Print_report'),

#----------------- Suspense Report-------------------------------------
    path('suspense_report',suspense_report, name='suspense_report'),
    path('create_suspense_collection/<uuid:id>/<str:date>/', create_suspense_collection, name='create_suspense_collection'),
    path('suspense_report_excel',suspense_report_excel, name='suspense_report_excel'),
    path('suspense_report_print',suspense_report_print, name='suspense_report_print'),
#------------------DSR Cash Sales Report-------------------------------------
    path('cashsales_report',cashsales_report, name='cashsales_report'),
    path('cashsales_report_print',cashsales_report_print, name='cashsales_report_print'),
    
#------------------DSR Credit Sales Report-------------------------------------
    path('creditsales_report',creditsales_report, name='creditsales_report'),
    path('creditsales_report_print',creditsales_report_print, name='creditsales_report_print'),
#-------------------DSR coupon Book  Sales-------------------------
    path('dsr_coupon_sales',dsr_coupon_sales, name='dsr_coupon_sales'),
    path('dsr_coupons_sales_print',dsr_coupons_sales_print, name='dsr_coupons_sales_print'),
        
#-------------------DSR coupon Book  Sales-------------------------
    path('dsr_coupon_book_sales',dsr_coupon_book_sales, name='dsr_coupon_book_sales'),
    path('dsr_coupon_book_sales_print',dsr_coupon_book_sales_print, name='dsr_coupon_book_sales_print'),
    
#-------------------DSR FOC Customers-------------------------
    path('dsr_foc_customers',dsr_foc_customers, name='dsr_foc_customers'),   
    path('dsr_foc_customers_print',dsr_foc_customers_print, name='dsr_foc_customers_print'),   

     
#------------------DSR Stock Report-------------------------------------
    path('dsr_stock_report',dsr_stock_report, name='dsr_stock_report'),
    path('dsr_stock_report_print',dsr_stock_report_print, name='dsr_stock_report_print'),
#------------------dsr_expense----------------
    path('dsr_expense',dsr_expense, name='dsr_expense'),
    path('dsr_expense_print',dsr_expense_print, name='dsr_expense_print'),
    path('dsr_five_gallon_rates',dsr_five_gallon_rates, name='dsr_five_gallon_rates'),
    path('dsr_five_gallon_rates_print',dsr_five_gallon_rates_print, name='dsr_five_gallon_rates_print'),
    path('dsr_credit_outstanding',dsr_credit_outstanding, name='dsr_credit_outstanding'),
    path('dsr_credit_outstanding_print',dsr_credit_outstanding_print, name='dsr_credit_outstanding_print'),
    
#------------------DSR Visit Statistics Report-------------------------------------
    path('visitstatistics_report',visitstatistics_report, name='visitstatistics_report'),
    path('visitstatistics_print',visitstatistics_report_print, name='visitstatistics_report_print'),
    
    #------------------DSR Five Gallon Related Report-------------------------------------
    path('fivegallonrelated_report/', fivegallonrelated_report, name='fivegallonrelated_report'),
    
    #------------------DSR Bottle Count 5gallon empty +fresh Report-------------------------------------
    path('bottlecount_report/', bottlecount_report, name='bottlecount_report'),
    
    path('dsr-summary/', dsr_summary, name='dsr_summary'),
    path('print-dsr-summary/', print_dsr_summary, name='print_dsr_summary'),
    # path('export-dsr-summary/', export_daily_summary_report, name='export_dsr_summary'),
    
    #------------------------------Bottle Count-------------------------------------
    path('van-route-bottle-count/', van_route_bottle_count, name='van_route_bottle_count'),
    path('vans-route-bottle-count-add/<uuid:pk>/',VansRouteBottleCountAdd, name='bottle_count_add'),
    path('vans-route-bottle-count-deduct/<uuid:pk>/',VansRouteBottleCountDeduct, name='bottle_count_deduct'),
    
    
    #------------------DSR Outstanding Amount Collected Report-------------------------------------
    path('outstanding_amount_collected',outstanding_amount_collected, name='outstanding_amount_collected'),

]