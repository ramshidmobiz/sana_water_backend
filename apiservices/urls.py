from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    ########################## Account ########################
    path('register/',UserSignUpView.as_view()),
    path('register/<int:id>/',UserSignUpView.as_view()),
    path('login/',Login_Api.as_view()),
    # Customer Sign in
    path('customers/',Customer_API.as_view()),
    path('customers/<str:id>/',Customer_API.as_view()),
    #################Master Url##############################
    

    path('route/<str:id>/',RouteMaster_API.as_view()),
    path('route/',RouteMaster_API.as_view())  ,

    path('location/<str:id>/',LocationMaster_API.as_view()),
    path('location/',LocationMaster_API.as_view()) ,

    path('designation/<str:id>/',DesignationMaster_API.as_view()),
    path('designation/',DesignationMaster_API.as_view()),

    path('branch/<str:id>/',BranchMaster_API.as_view()),
    path('branch/',BranchMaster_API.as_view()),

    path('category/<str:id>/',CategoryMaster_API.as_view()),
    path('category/',CategoryMaster_API.as_view()),

    path('emirates/<str:id>/',EmirateMaster_API.as_view()),
    path('emirates/',EmirateMaster_API.as_view()),

    ###################Product Url#######################

    path('product/',Product_API.as_view()),
    path('product/<str:id>/',Product_API.as_view()),
    path('product_price/',Product_Default_Price_API.as_view()),
    path('product_price/<str:id>/',Product_Default_Price_API.as_view()),

    #######################Van Url#################################

    path('van/',Van_API.as_view()),
    path('van/<str:id>/',Van_API.as_view()),
    path('assign_route/',Route_Assign.as_view()),

    path('schedule_by_route/<str:route_id>/<str:date_str>/<str:trip>', ScheduleByRoute.as_view()),
    path('schedule_view/<str:date_str>', ScheduleView.as_view()),
    
    ####################### Customer_Url s#################################

    path('customer_custody_item/',Customer_Custody_Item_API.as_view()),

    ##############################Van app####################################

    # Staff punch in and punch out
    path('staff_punch_in_api/', PunchIn_Api.as_view(), name='staff_punch_in_api'),
    path('staff_punch_out_api/', PunchOut_Api.as_view(), name='staff_punch_out_api'),
    path('location_emirates/', location_based_on_emirates, name='location-based-on-emirates'),
    path('staff_assigned_routes/',Route_Assign_Staff_Api.as_view(), name='staff_assigned_routes'),
    path('create/customer/',Create_Customer.as_view()),
    path('create/customer/<str:id>/',Create_Customer.as_view()),
    path('get_items_api/<str:id>/',Get_Items_API.as_view()),
    path('add_custody_item/',Add_Customer_Custody_Item_API.as_view()),
    path('add_custody_item/<str:id>/',Add_Customer_Custody_Item_API.as_view()),
    path('add_no_of_coupons/', Add_No_Coupons.as_view()),
    path('add_no_of_coupons/<str:id>/', Add_No_Coupons.as_view()),



    ################### COUPON MANAGEMENT URL ######################
    path('couponType/',CouponType_API.as_view()),
    path('couponType/<str:id>',CouponType_API.as_view()),
    path('coupon/',Coupon_API.as_view()),
    path('coupon/<str:id>',Coupon_API.as_view()),
    path('couponRequest/',CouponRequest_API.as_view()),
    path('assignStaffCoupon/',AssignStaffCoupon_API.as_view()),
    path('assignToCustomer/',AssigntoCustomer_API.as_view()),


    path('staff_new_order_api/', Staff_New_Order.as_view()),
    path('customer_create/',Customer_Create.as_view()),
    path('customer_details/<str:id>/',CustomerDetails.as_view()),
    path('check_customer', Check_Customer.as_view(), name='check_customer'),
    path('verify_otp', Verify_otp.as_view(), name='verify_otp'),

    # client_management
    path('vacations/', VacationListAPI.as_view(), name='vacation_list_api'),
    path('vacations/add/', VacationAddAPI.as_view(), name='vacation_add_api'),
    path('vacations/<uuid:vacation_id>/', VacationEditAPI.as_view(), name='vacation_edit_api'),
    path('vacations/<uuid:vacation_id>/delete/', VacationDeleteAPI.as_view(), name='vacation_delete_api'),
    
    path('myclient/',Myclient_API.as_view()),

    # path('add_customer_custody', CustomerCustody_API.as_view()),
    path('get_custody_item/', GetCustodyItem_API.as_view(), name='get_custody_item'),
    path('add_custody_item/', AddCustomerCustodyItem.as_view(), name='add_custody_item'),
    path('get_category/', GetCategoryAPI.as_view(), name='get_category'),
    path('get_products/', GetProductsAPI.as_view(), name='get_products'),
    path('custody_add/', Custody_Add_API.as_view(), name='custody_add'),

    

]
