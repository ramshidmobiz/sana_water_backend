from django.urls import path
from .views import *



urlpatterns = [
    path('van',van, name='van'),
    path('create_van/',create_van, name='create_van'),
    path('view_van/<uuid:van_id>/', view_van, name="view_van"),
    path('edit_van/<uuid:van_id>/', edit_van, name="edit_van"),

    #--Need to remove Start ----
    path('delete_van/<uuid:van_id>/', delete_van, name='delete_van'),
    path('van_assign/', view_association, name='van_assign'),
    path('create_assign/', create_association, name='create_association'),
    path('edit_assign/<uuid:van_id>/', edit_assign, name='edit_assign'),
    path('delete_assign/<uuid:van_id>/', delete_assign, name='delete_assign'),
    # Need to remove End------
    
    path('route_assign/<str:van_id>', route_assign, name="route_assign"),
    path('delete_route_assign', delete_route_assign, name="delete_route_assign"),

    path('licence_list', Licence_List.as_view(), name="licence_list"),
    path('licence_add', Licence_Adding.as_view(), name="licence_add"),
    path('licence_edit/<str:pk>/', License_Edit.as_view(), name='licence_edit'),
    path('licence_delete/<str:plate>/', licence_delete, name='licence_delete'),

    path('schedule_view', schedule_view, name="schedule_view"),
    path('schedule_by_route/<str:def_date>/<uuid:route_id>/<str:trip>', schedule_by_route, name="schedule_by_route"),
    
    path('pdf_download/<uuid:route_id>/<str:def_date>/<str:trip>', pdf_download, name="pdf_download"),
    path('excel_download/<uuid:route_id>/<str:def_date>/<str:trip>', excel_download, name="excel_download"),
    
]