from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login',user_login, name='login'),
    path('users', Users_List.as_view(), name='users'),
    path('user_create',User_Create.as_view(), name='user_create'),
    path('user_edit/<str:pk>', User_Edit.as_view(), name='user_edit'),
    path('user_details/<str:pk>', User_Details.as_view(), name='user_details'),

    path('customers', Customer_List.as_view(), name='customers'),
    path('customer_create',create_customer, name='customer_create'),
    path('customer_details/<str:pk>', Customer_Details.as_view(), name='customer_details'),
    path('edit_customer/<str:pk>',edit_customer, name='edit_customer'),

    path('visit_days_assign/<str:customer_id>', visit_days_assign, name="visit_days_assign"),


]