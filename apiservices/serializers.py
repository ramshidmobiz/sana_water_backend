
from customer_care.models import DiffBottlesModel
from rest_framework import serializers
#from . models import *
from rest_framework.views import APIView

from master.models  import *
from product.models  import * 
from client_management.models  import * 
from accounts.serializers import *
from van_management.serializers import *
from order.models import *

class CustomerCustodyItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustodyCustomItems
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
        model = CustodyCustomItems
        fields = '__all__'

class CustodyItemSerializers(serializers.ModelSerializer):
    product = Products_Serializers()
    class Meta:
        model = CustodyCustomItems
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

from client_management.models import CustodyCustomItems

class Category_Serializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryMaster
        fields = ['category_id','category_name']

class Product_Serializer(serializers.ModelSerializer):
    category_id=Category_Serializer()
    class Meta:
        model = Product
        fields =  [ 'product_name','category_id']
       

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CategoryMasterSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = CategoryMaster
        fields = ['category_id', 'category_name', 'products']

    def get_products(self, category_master):
        products = category_master.prod_category.all()
        return ProductSerializer(products, many=True).data
    
class CustodyCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = ['customer_id','customer_name'] 

class CustodyCustomItemsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustodyCustomItems
        fields = ['id', 'custody_custom', 'product', 'quantity', 'serialnumber', 'amount']

class CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = '__all__'


# coupon sales
class LowerCouponCustomersSerializer(serializers.ModelSerializer):
    last_coupon_type = serializers.SerializerMethodField()
    last_coupon_rate = serializers.SerializerMethodField()

    class Meta:
        model = Customers
        fields = '__all__'
        read_only_fields = ['id']
        
    def get_last_coupon_type(self, obj):
        coupon_type = ""
        if (coupon_type:=CustomerCoupon.objects.filter(customer=obj)).exists():
            coupon_type = coupon_type.latest('created_date').coupon.coupon_type.coupon_type_name
        return coupon_type
    
    def get_last_coupon_rate(self, obj):
        coupon_rate = ""
        if (coupon_rate:=CustomerCoupon.objects.filter(customer=obj)).exists():
            coupon_rate = coupon_rate.latest('created_date').rate
        return coupon_rate


class RechargeCustomerCouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerCoupon
        fields = ['customer','coupon','rate']

class CustomerCouponPaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerCouponPayment
        fields = "__all__"
        read_only_fields = ['id','customer_coupon']

class CashCouponPaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CashCouponPayment
        fields = "__all__"
        read_only_fields = ['id','customer_coupon_payment']

class ChequeCouponPaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChequeCouponPayment
        fields = "__all__"
        read_only_fields = ['id','customer_coupon_payment']

class ProdutItemMasterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProdutItemMaster
        fields = ['product_name']

class ProductSerializer(serializers.ModelSerializer):
    product_name = ProdutItemMasterSerializer()
    class Meta:
        model = Product
        fields = ['product_id', 'product_name','quantity']


class CustodyCustomItemListSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CustodyCustomItems
        fields = '__all__'

class CustodyCustomReturnSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerReturn
        fields = '__all__'


class ProdutItemMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProdutItemMaster
        fields =['id', 'product_name']


class CustodyCustomItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustodyCustomItems
        fields = '__all__'

class SupplyItemFiveCanWaterProductGetSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['product_id', 'product_name', 'rate', 'quantity', 'return_for_today', 'total_to_return']
        read_only_fields = ['product_id', 'product_name', 'rate', 'quantity', 'return_for_today', 'total_to_return']

    def get_rate(self, obj):
        customer_id = self.context.get('customer_id')
        try:
            customer = Customers.objects.get(pk=customer_id)
            rate = customer.rate
        except Customers.DoesNotExist:
            rate = obj.rate
        return rate

class SupplyItemFiveGallonWaterGetSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()

    class Meta:
        model = ProdutItemMaster
        fields = ['id', 'product_name','category','unit','rate','quantity']
        read_only_fields = ['id', 'product_name']

    def get_rate(self, obj):
        customer_id = self.context.get('customer_id')
        try:
            customer = Customers.objects.get(pk=customer_id)
            rate = customer.rate
        except Customers.DoesNotExist:
            rate = Product.objects.filter(product_name=obj).latest('created_date').rate
        return rate
    
    def get_quantity(self, obj):
        customer_id = self.context.get('customer_id')
        try:
            customer = Customers.objects.get(pk=customer_id)
            qty = customer.no_of_bottles_required
        except Customers.DoesNotExist:
            qty = 1
        
        if (reuests:=DiffBottlesModel.objects.filter(delivery_date__date=date.today(), customer__pk=customer_id)).exists():
            for r in reuests :
                if r.request_type.request_name == "5 Gallon":
                    qty = qty + r.quantity_required
        return qty
    
class SupplyItemProductGetSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()

    class Meta:
        model = ProdutItemMaster
        fields = ['id', 'product_name','category','unit','rate','quantity']
        read_only_fields = ['id', 'product_name']

    def get_rate(self, obj):
        rate = Product.objects.filter(product_name=obj).latest('created_date').rate
        return rate
    
    def get_quantity(self, obj):
        customer_id = self.context.get('customer_id')
        qty = 1
        if (reuests:=DiffBottlesModel.objects.filter(delivery_date__date=date.today(), customer__pk=customer_id)).exists():
            for r in reuests :
                if r.request_type.request_name == "5 Gallon":
                    qty = r.quantity_required
        return qty

class SupplyItemCustomersSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    class Meta:
        model = Customers
        fields = '__all__'
        
    def get_products(self, obj):
        fivegallon = ProdutItemMaster.objects.get(product_name="5 Gallon")
        five_gallon_serializer = SupplyItemFiveGallonWaterGetSerializer(fivegallon, context={"customer": obj.pk})
        five_gallon_data = five_gallon_serializer.data
        
        supply_product_data = []
        
        c_requests = DiffBottlesModel.objects.filter(delivery_date__date=date.today(), customer__pk=obj.pk, request_type__request_name__in=['1L Pet Bottle','Coolers','Water Cooler','Dispenser'])
        if c_requests.exists():
            for r in c_requests:
                items = ProdutItemMaster.objects.filter(product_name=r.request_type.request_name)
                if items.exists():
                    supply_product_serializer = SupplyItemProductGetSerializer(items.first(), many=False)
                    supply_product_data.append(supply_product_serializer.data)
        
        return [five_gallon_data] + supply_product_data

class CustomerSupplySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomerSupply
        fields = ['id', 'customer', 'salesman', 'grand_total', 'discount', 'net_payable', 'vat', 'subtotal', 'amount_recieved', 'created_by', 'created_date', 'modified_by', 'modified_date']
        read_only_fields = ['id', 'created_by', 'created_date', 'modified_by', 'modified_date']

class CustomerSupplyItemsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  # Assuming you have a serializer for the Product model

    class Meta:
        model = CustomerSupplyItems
        fields = ['id', 'customer_supply', 'product', 'quantity', 'amount']
        read_only_fields = ['id']

class CustomerSupplyStockSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  # Assuming you have a serializer for the Product model
    customer = CustomersSerializer()  # Assuming you have a serializer for the Customers model

    class Meta:
        model = CustomerSupplyStock
        fields = ['id', 'product', 'customer', 'stock_quantity']
        read_only_fields = ['id']


class CustomerCouponStockSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomerCouponStock
        fields = ['id', 'coupon_type_id', 'count', 'customer_name']
        read_only_fields = ['id']
        
    def get_customer_name(self, obj):
        return obj.customer.customer_name

class VanCouponStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutstandingAmount
        fields = '__all__'


class OutstandingCouponSerializer(serializers.ModelSerializer):
    custodycustomitems = CustodyCustomItemSerializer
    class Meta:
        model = OutstandingAmount
        fields = '__all__'
class OutstandingAmountSerializer(serializers.ModelSerializer):
    custodycustomitems = CustodyCustomItemSerializer
    class Meta:
        model = OutstandingAmount
        fields = '__all__'


class VanCouponStockSerializer(serializers.ModelSerializer):
    book_no = serializers.SerializerMethodField()
    number_of_coupons = serializers.SerializerMethodField()
    number_of_free_coupons = serializers.SerializerMethodField()
    total_number_of_coupons = serializers.SerializerMethodField()
    coupon_method = serializers.SerializerMethodField()
    coupon_type = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField()
    
    class Meta:
        model = VanCouponStock
        fields = '__all__'
        
    def get_book_no(self, obj):
        return obj.coupon.book_num
    
    def get_number_of_coupons(self, obj):
        return obj.coupon.no_of_leaflets
    
    def get_number_of_free_coupons(self, obj):
        return obj.coupon.free_leaflets
    
    def get_total_number_of_coupons(self, obj):
        return int(obj.coupon.no_of_leaflets) + int(obj.coupon.free_leaflets)
    
    def get_coupon_method(self, obj):
        return obj.coupon.coupon_method
    
    def get_coupon_type(self, obj):
        coupon_type = CouponType.objects.get(pk=obj.coupon.coupon_type_id).coupon_type_name
        return coupon_type
    
    def get_rate(self, obj):
        product_item = ProdutItemMaster.objects.get(product_name=obj.coupon.coupon_type.coupon_type_name)
        rate = Product.objects.filter(product_name=product_item).latest("created_date").rate
        return rate
        
class VanProductStockSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    class Meta:
        model = VanProductStock
        fields = '__all__'
        
    def get_product_name(self, obj):
        return obj.product.product_name
    






# class CustomerCouponStockSerializer(serializers.ModelSerializer):
#     customer_name = serializers.CharField(source='customer.customer_name', read_only=True)
#     coupon_type_name = serializers.CharField(source='coupon_type_id.coupon_type_name', read_only=True)
#
#     class Meta:
#         model = CustomerCouponStock
#         fields = ['customer', 'count', 'coupon_type_id']

class CustomerOutstandingSerializer(serializers.Serializer):
    customer = serializers.UUIDField()
    customer_name = serializers.CharField(max_length=200)
    building_name = serializers.CharField(max_length=200)
    route_name = serializers.CharField(max_length=200)
    route_id = serializers.UUIDField()
    door_house_no = serializers.CharField(max_length=200)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    empty_can = serializers.DecimalField(max_digits=10, decimal_places=2)
    coupons = serializers.DecimalField(max_digits=10, decimal_places=2)
#         fields = ['customer_name', 'count', 'coupon_type_id', 'coupon_type_name']


class CouponTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponType
        fields = '__all__'
        read_only_fields = ['id', 'coupon_type_name']
class RouteMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteMaster
        fields = ['route_name']
# def get_user_id(self, obj):
#     user = self.context.get('request').user
#     if user.user_type == 'Salesman':
#         return user.id
#     return None

class CustomerCouponCountSerializer(serializers.ModelSerializer):
    # customer_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomerCouponStock
        fields = ['id', 'coupon_type_id', 'count']
        read_only_fields = ['id']

    def get_customer_name(self, obj):
        return obj.customer.customer_name
class CustomerDetailSerializer(serializers.ModelSerializer):
    coupon_count = serializers.SerializerMethodField()
    route_name = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()

    def get_user_id(self, obj):
        request = self.context.get('request')

        if request and hasattr(request, 'user') and request.user.is_authenticated:
            if request.user.user_type == 'Salesman':
                # If the user is a salesman, return the user ID
                return request.user.id
        return None

    def get_route_name(self, obj):
        if obj.routes:
            return obj.routes.route_name
        return None

    def get_coupon_count(self, obj):
        counts = CustomerCouponStock.objects.filter(customer=obj)
        return CustomerCouponCountSerializer(counts, many=True).data

    class Meta:
        model = Customers
        fields = ['customer_id','customer_name', 'coupon_count', 'route_name', 'user_id']
