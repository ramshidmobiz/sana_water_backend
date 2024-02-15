from django.urls import path
from .views import *

urlpatterns = [
        path('customer_custody_item/<str:customer_id>', customer_custody_item, name='customer_custody_item'),
        path('get_custody_items', get_custody_items, name='get_custody_items'),
        path('create-custody-item/', create_custody_item, name='create_custody_item'),


        #vacation
        path('vacation_list', vacation_list, name="vacation_list"),
        path('vacation_add', Vacation_Add.as_view(), name="vacation_add"),
        path('vacation_edit/<uuid:vacation_id>', Vacation_Edit.as_view(), name='vacation_edit'),
        path('vacation_delete/<uuid:vacation_id>',  Vacation_Delete.as_view(), name="vacation_delete"),
        
        path('vacation_route',  RouteSelection.as_view(), name="vacation_route"),    

        path('custody_item_list', Custody_ItemListView.as_view(), name='custody_item_list'),
        path('add_category_list<str:pk>', Add_CategoryListView.as_view(), name='add_category_list'),
        path('get_category_list', Get_CategoryListView.as_view(), name='get_category_list'),
        path('get_rate', GetRateView.as_view(), name='get_rate'),
        path('added_list', AddListView.as_view(), name='added_list'),

        path('pullout_list<str:pk>', PulloutListView.as_view(), name='pullout_list'),



   
]