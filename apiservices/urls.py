from django.conf import settings
from django.urls import path,re_path
from django.conf.urls.static import static

from . views import *
from . import views

urlpatterns = [

#     ########################## Account ########################
#     path('register/',UserSignUpView.as_view()),
#     path('register/<int:id>/',UserSignUpView.as_view()),
#     path('login/',Login_Api.as_view()),
#     # Customer Sign in
#     path('customers/',Customer_API.as_view()),
#     path('customers/<str:id>/',Customer_API.as_view()),
#     #################Master Url##############################

#     path('route/<str:id>/',RouteMaster_API.as_view()),
#     path('route/',RouteMaster_API.as_view())  ,

#     path('location/<str:id>/',LocationMaster_API.as_view()),
#     path('location/',LocationMaster_API.as_view()) ,

#     path('designation/<str:id>/',DesignationMaster_API.as_view()),
#     path('designation/',DesignationMaster_API.as_view()),

#     path('branch/<str:id>/',BranchMaster_API.as_view()),
#     path('branch/',BranchMaster_API.as_view()),

#     path('category/<str:id>/',CategoryMaster_API.as_view()),
#     path('category/',CategoryMaster_API.as_view()),

#     path('emirates/<str:id>/',EmirateMaster_API.as_view()),
#     path('emirates/',EmirateMaster_API.as_view()),

#     ###################Product Url#######################

#     path('product/',Product_API.as_view()),
#     path('product/<str:id>/',Product_API.as_view()),
#     path('product_price/',Product_Default_Price_API.as_view()),
#     path('product_price/<str:id>/',Product_Default_Price_API.as_view()),

#     #######################Van Url#################################

#     path('van/',Van_API.as_view()),
#     path('van/<str:id>/',Van_API.as_view()),
#     path('assign_route/',Route_Assign.as_view()),

#     path('schedule_by_route/<str:route_id>/<str:date_str>/<str:trip>', ScheduleByRoute.as_view()),
#     path('schedule_view/<str:date_str>/', ScheduleView.as_view()),


#     path('expense_heads/', ExpenseHeadListAPI.as_view(), name='expensehead-list'),
#     path('expense_heads/<uuid:pk>/', ExpenseHeadDetailAPI.as_view(), name='expensehead-detail'),

#     path('expenses/', ExpenseListAPI.as_view(), name='expense-list'),
#     path('expenses/<uuid:expense_id>/', ExpenseDetailAPI.as_view(), name='expense-detail'),

#     # Order change and return
#     path('change_reason/', ChangeReasonListAPI.as_view(), name='change_reason'),
#     path('change_reason/<int:change_reason_id>', ChangeReasonDetailAPI.as_view(), name="change_reason_detai"),

#     path('order_change/', OrderChangeListAPI.as_view(), name='order_change'),
#     path('order_change/<uuid:order_change_id>', OrderChangeDetailAPI.as_view(), name="order_change_detai"),

#     path('order_return/', OrderReturnListAPI.as_view(), name='order_return'),
#     path('order_return/<uuid:order_return_id>', OrderReturnDetailAPI.as_view(), name="order_return_detai"),  

    
#     ####################### Customer_Url s#################################

#     path('customer_custody_item/',Customer_Custody_Item_API.as_view()),

#     ##############################Van app####################################

#     # Staff punch in and punch out
#     path('staff_punch_in_api/', PunchIn_Api.as_view(), name='staff_punch_in_api'),
#     path('staff_punch_out_api/', PunchOut_Api.as_view(), name='staff_punch_out_api'),
#     path('location_emirates/', location_based_on_emirates, name='location-based-on-emirates'),
#     path('staff_assigned_routes/',Route_Assign_Staff_Api.as_view(), name='staff_assigned_routes'),
#     path('create/customer/',Create_Customer.as_view()),
#     path('create/customer/<str:id>/',Create_Customer.as_view()),
#     path('get_items_api/<str:id>/',Get_Items_API.as_view()),
#     path('add_custody_item/',Add_Customer_Custody_Item_API.as_view()),
#     path('add_custody_item/<str:id>/',Add_Customer_Custody_Item_API.as_view()),
#     path('add_no_of_coupons/', Add_No_Coupons.as_view()),
#     path('add_no_of_coupons/<str:id>/', Add_No_Coupons.as_view()),
    
#     # supply
#     re_path(r'^supply-product/(?P<customer_id>.*)/(?P<product_id>.*)/$', views.supply_product),
#     re_path(r'^create-customer-supply/$', views.create_customer_supply),
    
#     ################### COUPON MANAGEMENT URL ######################
#     path('couponType/',CouponType_API.as_view()),
#     path('couponType/<str:id>',CouponType_API.as_view()),
#     path('coupon/',Coupon_API.as_view()),
#     path('coupon/<str:id>',Coupon_API.as_view()),
#     path('couponRequest/',CouponRequest_API.as_view()),
#     path('assignStaffCoupon/',AssignStaffCoupon_API.as_view()),
#     path('assignToCustomer/',AssigntoCustomer_API.as_view()),
    
#     # coupon recharge
#     path('get-lower-coupon-customers/', views.get_lower_coupon_customers),
#     path('fetch-coupon-data/', views.fetch_coupon),
#     path('customer-coupon-recharge/', views.customer_coupon_recharge),
    
#     path('customer-coupon-stock/', views.customer_coupon_stock),
    
#     path('product-items/', views.product_items),
#     path('staff_new_order_api/', Staff_New_Order.as_view()),
#     path('customer_create/',Customer_Create.as_view()),
#     path('customer_details/<str:id>/',CustomerDetails.as_view()),
#     path('check_customer', Check_Customer.as_view(), name='check_customer'),
#     path('verify_otp', Verify_otp.as_view(), name='verify_otp'),

#     # client_management
#     path('vacations/', VacationListAPI.as_view(), name='vacation_list_api'),
#     path('vacations/add/', VacationAddAPI.as_view(), name='vacation_add_api'),
#     path('vacations/<uuid:vacation_id>/', VacationEditAPI.as_view(), name='vacation_edit_api'),
#     path('vacations/<uuid:vacation_id>/delete/', VacationDeleteAPI.as_view(), name='vacation_delete_api'),
    
#     path('myclient/',Myclient_API.as_view()),
#     path('get_products/', GetProductAPI.as_view(), name='get_products'),
#     path('custody_tems/', CustodyCustomItemAPI.as_view(), name='custody_tems'),
#     path('custody_item_list/' ,CustodyCustomItemListAPI.as_view(), name='custody_item_list'),
#     path('custody_item_return/', CustodyItemReturnAPI.as_view(), name='custody_item_return'),

#     path('outstanding_amount/',OutstandingAmountAPI.as_view(), name = 'outstanding_amount'),
#     path('outstanding_amount_list/',OutstandingAmountListAPI.as_view(), name = 'outstanding_amount_list'),
#     # path('outstanding_coupon/',OutstandingCouponAPI.as_view(), name = 'outstanding_coupon'),

#     path('vanstock-list/', VanStockAPI.as_view()),






    

    

]
