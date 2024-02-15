
from rest_framework import serializers
#from . models import *
from master.models  import * 
from product.models  import * 
from client_management.models  import * 
from accounts.serializers import *
from van_management.serializers import *
from order.models import *

class CustomerCustodyItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = Customer_Custody_Items
        fields = '__all__'

class Attendance_Serializers(serializers.ModelSerializer):
    staff = CustomUserSerializers()

    class Meta:
        model = Attendance_Log
        fields = ['attendance_id', 'punch_in_date', 'punch_in_time', 'punch_out_date', 'punch_out_time', 'staff']

class Staff_Assigned_Route_Details_Serializer(serializers.ModelSerializer):

    class Meta:
        model = RouteMaster
        fields = ['route_id','route_name','branch_id']


class Product_Category_Serializers(serializers.ModelSerializer):

    class Meta:
        model = CategoryMaster
        fields = ['category_id','category_name']

class Products_Serializers(serializers.ModelSerializer):
    category_id = Product_Category_Serializers()

    class Meta:
        model = Product
        fields = ['product_id','product_name','rate','category_id']

class Items_Serializers(serializers.ModelSerializer):
    product_id = Products_Serializers()

    class Meta:
        model = Product_Default_Price_Level
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = '__all__'

class CustomerCustodyItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer_Custody_Items
        fields = '__all__'

class CustodyItemSerializers(serializers.ModelSerializer):
    product = Products_Serializers()
    class Meta:
        model = Customer_Custody_Items
        fields = '__all__'

class CustomerInhandCouponsSerializers(serializers.ModelSerializer):

    class Meta:
        model = Customer_Inhand_Coupons
        fields = '__all__'

class GetCustomerInhandCouponsSerializers(serializers.ModelSerializer):
    customer = CustomerSerializer()
    class Meta:
        model = Customer_Inhand_Coupons
        fields = '__all__'

class StaffOrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Staff_Orders
        fields = '__all__'

class StaffOrderDetailsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Staff_Orders_details
        fields = '__all__'
class CustomerOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer_Order
        fields = '__all__'

from client_management.models import Customer_Custody_Items

class Category_Serializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryMaster
        fields = ['category_id','category_name']

class Product_Serializer(serializers.ModelSerializer):
    category_id=Category_Serializer()
    class Meta:
        model = Product
        fields =  [ 'product_name','category_id']

# class CustomerCustodyItemSerializer(serializers.ModelSerializer):
#     product = Product_Serializer()
#     class Meta:
#         model = Customer_Custody_Items
#         fields = [ 'product', 'serialnumber','count']

class SelectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryMaster
        fields = ['category_id','category_name']


class SelectProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id','product_name']

class CustomerCustodyItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer_Custody_Items
        fields = '__all__'