from django.urls import path
from .views import *

urlpatterns = [
path('requesttype_list', RequestType_List.as_view(), name='requesttype_list'),
path('requesttype_create',RequestType_Create.as_view(), name='requesttype_create'),
path('requesttype_edit/<str:pk>', RequestType_Edit.as_view(), name='requesttype_edit'),
path('requesttype_details/<str:pk>', RequestType_Details.as_view(), name='requesttype_details'),

path('bottle_list/<str:pk>', Bottle_List.as_view(), name='bottle_list'),
path('diffbottles_create/<str:pk>', Diffbottles_Create.as_view(), name='diffbottles_create'),

path('coupon_purchase_list/<str:pk>', Coupon_Purchse_List.as_view(), name='coupon_purchase_list'),
path('coupon_purchase_create/<str:pk>', Coupon_Purchse_Create.as_view(), name='coupon_purchase_create'),

path('other_list/<str:pk>', Other_List.as_view(), name='other_list'),
path('otherreq_create/<str:pk>', Other_Req_Create.as_view(), name='otherreq_create'),

path('custody_pullout_list/<str:pk>', Custody_Pullout_List.as_view(), name='custody_pullout_list'),
path('custody_pullout_create/<str:pk>', Custody_Pullout_Create.as_view(), name='custody_pullout_create'),
path('get_item_quantity',get_item_quantity, name='get_item_quantity'),

path('requestType',requestType, name='requestType'),
path('custody_pullout/<str:pk>',custody_pullout, name='custody_pullout'),
path('change_of_address/<str:pk>',change_of_address, name='change_of_address'),
path('default_bottle_qty/<str:pk>',default_bottle_qty, name='default_bottle_qty'),

#create customer
path('createcustomer',createcustomer, name='createcustomer'),

]