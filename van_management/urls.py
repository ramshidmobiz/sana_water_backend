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

    # Expense
    path('expensehead_list', ExpenseHeadList.as_view(), name="expensehead_list"),
    path('expensehead_add', ExpenseHeadAdd.as_view(), name="expensehead_add"),
    path('expensehead_edit/<uuid:expensehead_id>', ExpenseHeadEdit.as_view(), name="expensehead_edit"),
    path('expensehead_delete/<uuid:expensehead_id>', ExpenseHeadDelete.as_view(), name="expensehead_delete"),


    path('expense_list', ExpenseList.as_view(), name="expense_list"),
    path('expense_add', ExpenseAdd.as_view(), name="expense_add"),
    path('expense_edit/<uuid:expense_id>', ExpenseEdit.as_view(), name="expense_edit"),
    path('expense_delete/<uuid:expense_id>', ExpenseDelete.as_view(), name="expense_delete"),
    
                                   
    # path('van-stock-product', VanStock.as_view(), name="vanstock"),
    # path('van-stock-product', VanStockList.as_view(), name="vanstock"),
    path('van-stock-product', VanProductStockList.as_view(), name="vanstock_product"),
    
    path('offload', offload, name="offload"),
    path('get-van-coupon-bookno/', get_van_coupon_bookno, name="get_van_coupon_bookno"),
    path('view_item_details/<str:pk>/', View_Item_Details.as_view(), name="view_item_details"),
    path('edit-product-count/<uuid:pk>/', EditProductView.as_view(), name="edit_product_count"),
    path('edit-coupon-count/<uuid:van_pk>/', EditCouponView.as_view(), name="edit_coupon_count"),
    
    path('salesman-requests/',salesman_requests, name="salesman_requests"),


    path('bottle_allocation/',BottleAllocationn, name='bottle_allocation'),
    path('edit_bottle_allocation/<uuid:route_id>/',EditBottleAllocation, name='edit_bottle_allocation'),

    path('vans_route_bottle_count/', VansRouteBottleCount, name='vans_route_bottle_count'),
    path('vans_route_bottle_count_add/<uuid:van_id>/',VansRouteBottleCountAdd, name='vans_route_bottle_count_add'),
    path('vans_route_bottle_count_deduct/<uuid:van_id>/',VansRouteBottleCountDeduct, name='vans_route_bottle_count_deduct'),

    path('van_coupon_stock/', VanCouponStockList.as_view(), name='van_coupon_stock'),



    
]