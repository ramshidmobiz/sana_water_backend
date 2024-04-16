from django.db.models import Sum, Subquery,Value
from django.db.models.functions import Coalesce
from rest_framework import serializers
#from . models import *
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from invoice_management.models import Invoice
from order.models import *
from master.models  import *
from product.models  import * 
from accounts.serializers import *
from client_management.models  import *
from sales_management.models import CollectionCheque, CollectionItems, CollectionPayment
from van_management.serializers import *
from customer_care.models import DiffBottlesModel

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
        if (coupon_type:=CustomerCouponItems.objects.filter(customer_coupon__customer=obj)).exists():
            coupon_type = coupon_type.latest('customer_coupon__created_date').coupon.coupon_type.coupon_type_name
        return coupon_type
    
    def get_last_coupon_rate(self, obj):
        coupon_rate = ""
        if (coupon_rate:=CustomerCouponItems.objects.filter(customer_coupon__customer=obj)).exists():
            coupon_rate = coupon_rate.latest('customer_coupon__created_date').rate
        return coupon_rate


class CustomerCouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerCoupon
        fields = ['customer','salesman']
        
class CustomerCouponItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerCouponItems
        fields = ['coupon','rate']

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


class ProdutItemMasterSerializerr(serializers.ModelSerializer):
    class Meta:
        model = ProdutItemMaster
        fields =['id', 'product_name']


class CustodyCustomItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name.product_name', read_only=True)
    deposit_type = serializers.CharField(source='custody_custom.deposit_type', read_only=True)
    agreement_number = serializers.CharField(source='custody_custom.agreement_no', read_only=True)
    
    class Meta:
        model = CustodyCustomItems
        fields = ['id', 'custody_custom', 'product', 'product_name', 'quantity', 'serialnumber', 'amount', 'deposit_type', 'agreement_number']

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
        fields = ['id', 'product_name','category','unit','rate','quantity','tax']
        read_only_fields = ['id', 'product_name']

    def get_rate(self, obj):
        customer_id = self.context.get('customer_id')
        if obj.product_name == "5 Gallon":
            try:
                customer = Customers.objects.get(pk=customer_id)
                rate = customer.rate
            except Customers.DoesNotExist:
                rate = obj.rate
        else:
            obj.rate
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
    

class CouponLeafSerializer(serializers.ModelSerializer):

    class Meta:
        model = CouponLeaflet
        fields = ['couponleaflet_id', 'leaflet_number','leaflet_name','used']
        read_only_fields = ['id']

class SupplyItemCustomersSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    pending_to_return = serializers.SerializerMethodField()
    coupon_details = serializers.SerializerMethodField()
    class Meta:
        model = Customers
        fields = ['customer_id','customer_name','routes','sales_type','products','pending_to_return','coupon_details']
        
    def get_products(self, obj):
        fivegallon = ProdutItemMaster.objects.get(product_name="5 Gallon")
        five_gallon_serializer = SupplyItemFiveGallonWaterGetSerializer(fivegallon, context={"customer_id": obj.pk})
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
    
    def get_pending_to_return(self, obj):
        # total_quantity = CustodyCustomItems.objects.filter(
        #     product__product_name="5 Gallon",
        #     custody_custom__customer=obj
        # ).aggregate(total_quantity=Sum('quantity'))['total_quantity']
        
        total_coupons = CustomerOutstandingReport.objects.filter(customer=obj,product_type="emptycan").aggregate(total=Coalesce(Sum('value'), Value(0)))['total']
        
        return total_coupons
    
    def get_coupon_details(self, obj):
        pending_coupons = 0
        digital_coupons = 0
        manual_coupons = 0
        leafs = []
        
        if CustomerOutstandingReport.objects.filter(product_type="coupons",customer=obj).exists() :
            pending_coupons = CustomerOutstandingReport.objects.get(product_type="coupons",customer=obj).value
        
        if CustomerCouponStock.objects.filter(customer=obj).exists() :
            customer_coupon_stock = CustomerCouponStock.objects.filter(customer=obj)
            
            if (customer_coupon_stock_digital:=customer_coupon_stock.filter(coupon_method="digital")).exists() :
                digital_coupons = customer_coupon_stock_digital.aggregate(total_count=Sum('count'))['total_count']
            if (customer_coupon_stock_manual:=customer_coupon_stock.filter(coupon_method="manual")).exists() :
                manual_coupons = customer_coupon_stock_manual.aggregate(total_count=Sum('count'))['total_count']
            
            coupon_ids_queryset = CustomerCouponItems.objects.filter(customer_coupon__customer=obj).values_list('coupon__pk', flat=True)
            coupon_leafs = CouponLeaflet.objects.filter(used=False,coupon__pk__in=list(coupon_ids_queryset))
            leafs = CouponLeafSerializer(coupon_leafs, many=True).data
            
        return {
            'pending_coupons': pending_coupons,
            'digital_coupons': digital_coupons,
            'manual_coupons': manual_coupons,
            'leafs' : leafs,   
        }

class CustomerSupplySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomerSupply
        fields = ['id', 'customer', 'salesman', 'grand_total', 'discount', 'net_payable', 'vat', 'subtotal', 'amount_recieved', 'created_by', 'created_date', 'modified_by', 'modified_date']
        read_only_fields = ['id', 'created_by', 'created_date', 'modified_by', 'modified_date']

class CustomerSupplyItemsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CustomerSupplyItems
        fields = ['id', 'customer_supply', 'product', 'quantity', 'amount']
        read_only_fields = ['id']

class CustomerSupplyStockSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  
    customer = CustomersSerializer()  

    class Meta:
        model = CustomerSupplyStock
        fields = ['id', 'product', 'customer', 'stock_quantity']
        read_only_fields = ['id']


class CustomerCouponStockSerializer(serializers.ModelSerializer):
    stock_id = serializers.SerializerMethodField()
    manual_count = serializers.SerializerMethodField()
    digital_count = serializers.SerializerMethodField()

    class Meta:
        model = Customers
        fields = ['customer_id','custom_id','customer_name','stock_id', 'manual_count', 'digital_count']
        
    def get_stock_id(self, obj):
        try :
            stock = CustomerCouponStock.objects.get(customer=obj).pk
        except:
            stock = ""
        return stock
    
    def get_manual_count(self, obj):
        if CustomerCouponStock.objects.filter(customer=obj,coupon_method='manual').exists():
            return  CustomerCouponStock.objects.get(customer=obj,coupon_method='manual').count
        else:
            return 0
    
    def get_digital_count(self, obj):
        if CustomerCouponStock.objects.filter(customer=obj,coupon_method='digital').exists():
            return  CustomerCouponStock.objects.get(customer=obj,coupon_method='digital').count
        else:
            return 0


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
        fields = ['id','coupon','stock_type','count','van','book_no','number_of_coupons','number_of_free_coupons','total_number_of_coupons','coupon_method','coupon_type','rate']
        
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
        return product_item.rate
        
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

class CustomerOutstandingSerializer(serializers.ModelSerializer):
    route_name = serializers.SerializerMethodField()
    route_id = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    empty_can = serializers.SerializerMethodField()
    coupons = serializers.SerializerMethodField()
    
    class Meta:
        model = Customers
        fields = ['customer_id','customer_name','building_name','route_name','route_id','door_house_no','amount','empty_can','coupons']
    
    def get_amount(self,obj):
        result = 0
        if (instances:=CustomerOutstandingReport.objects.filter(customer=obj,product_type="amount")).exists():
            result = instances.first().value
        return result
    
    def get_empty_can(self,obj):
        result = 0
        if (instances:=CustomerOutstandingReport.objects.filter(customer=obj,product_type="emptycan")).exists():
            result = instances.first().value
        return result
    
    def get_coupons(self,obj):
        result = 0
        if (instances:=CustomerOutstandingReport.objects.filter(customer=obj,product_type="coupons")).exists():
            result = instances.first().value
        return result
    
    def get_route_id(self,obj):
        return obj.routes.route_id
    
    def get_route_name(self,obj):
        return obj.routes.route_name

class CouponTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponType
        fields = ['coupon_type_id','coupon_type_name','no_of_leaflets','valuable_leaflets','free_leaflets']
        
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
    coupon_type_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomerCouponStock
        fields = ['id', 'coupon_type_id', 'coupon_type_name','count']
        read_only_fields = ['id']

    def get_coupon_type_name(self, obj):
        return obj.coupon_type_id.coupon_type_name
    
    
class CustomerDetailSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    coupon_count = serializers.SerializerMethodField()
    route_name = serializers.SerializerMethodField()
    total_count = serializers.SerializerMethodField()

    class Meta:
        model = Customers
        fields = ['customer_id','customer_name', 'route_name','user_id','total_count','coupon_count']
        
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
        return CustomerCouponCountSerializer(counts, many=True,context={"customer_id": obj.pk}).data
    
    def get_total_count(self, obj):
        total_count = CustomerCouponStock.objects.filter(customer=obj).aggregate(total_count=Sum('count'))['total_count']
        return total_count


class CustomerSerializer(serializers.ModelSerializer):
    route_name = serializers.SerializerMethodField()

    class Meta:
        model = Customers
        fields = ['id', 'customer_name', 'building_name', 'sales_type', 'route_name']

    def get_route_name(self, obj):
        if obj.routes:
            return obj.routes.route_name
        return None



# class CollectionSerializer(serializers.ModelSerializer):
#     route = RouteMasterSerializer(source='customer.routes', read_only=True)
#     customer_name = serializers.CharField(source='customer.customer_name')
#     billing_address = serializers.CharField(source='customer.billing_address')
#     mobile_no=serializers.CharField(source='customer.mobile_no')
#
#     class Meta:
#         model = CustomerSupply
#         fields = ['created_date', 'customer_name', 'salesman','mobile_no', 'grand_total', 'billing_address','route']
# class CollectionSerializer(serializers.ModelSerializer):
#     customer_name = serializers.CharField(source='customer.customer_name')
#     mobile_no = serializers.CharField(source='customer.mobile_no')
#     route_name = RouteMasterSerializer(source='customer.routes', read_only=True)

#     payment_method = serializers.ChoiceField(choices=CollectionPayment.PAYMENT_TYPE_CHOICES)
#     amount = serializers.DecimalField(max_digits=10, decimal_places=2)

#     class Meta:
#         model=CollectionPayment
#         fields='__all__'
        
class DashBoardSerializer(serializers.Serializer):
    total_schedule = serializers.DecimalField(max_digits=10, decimal_places=2)
    completed_schedule = serializers.DecimalField(max_digits=10, decimal_places=2)
    coupon_sale = serializers.DecimalField(max_digits=10, decimal_places=2)
    empty_bottles = serializers.DecimalField(max_digits=10, decimal_places=2)
    expences = serializers.DecimalField(max_digits=10, decimal_places=2)
    filled_bottles = serializers.DecimalField(max_digits=10, decimal_places=2)
    used_coupons = serializers.DecimalField(max_digits=10, decimal_places=2)
    cash_in_hand = serializers.DecimalField(max_digits=10, decimal_places=2)
    fields=['customer_name','mobile_no','payment_method','amount','route_name']

    def create(self, validated_data):
        customer_supply_data = validated_data.pop('customer_supply', None)
        if customer_supply_data:
            customer_supply = CustomerSupply.objects.create(**customer_supply_data)
            validated_data['customer_supply'] = customer_supply
        return super().create(validated_data)




class CollectionPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionPayment
        fields = '__all__'





# class RouteMasterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RouteMaster
#         fields = ['route_name']
# class CustomerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Customers
#         fields = ['customer_id']
#
# class CollectionSerializer(serializers.ModelSerializer):
#     customer_id = CustomerSerializer(source='customer', read_only=True)
#     invoice_id = serializers.SerializerMethodField()
#     payment_method = serializers.SerializerMethodField()
#     payment_amount = serializers.SerializerMethodField()
#     reference_no = serializers.SerializerMethodField()
#
#     class Meta:
#         model = CustomerSupply
#         fields = ['customer_id', 'created_date', 'grand_total', 'invoice_id', 'payment_method', 'payment_amount', 'reference_no']
#
#     def get_invoice_id(self, obj):
#         invoice = Invoice.objects.filter(customer=obj.customer).last()
#         return invoice.id if invoice else None
#
#     def get_payment_method(self, obj):
#         payment = CollectionPayment.objects.filter(customer_supply=obj).last()
#         return payment.payment_method if payment else None
#
#     def get_payment_amount(self, obj):
#         payment = CollectionPayment.objects.filter(customer_supply=obj).last()
#         return payment.amount if payment else None
#
#     def get_reference_no(self, obj):
#         invoice = Invoice.objects.filter(customer=obj.customer).last()
#         return invoice.reference_no if invoice else None


# class CollectionSerializer(serializers.ModelSerializer):
#     customer_id = serializers.CharField(source='customer.customer_id')
#     invoices = serializers.SerializerMethodField()
#
#     class Meta:
#         model = CustomerSupply
#         fields = ['customer_id', 'invoices']
#
#     def get_invoices(self, obj):
#         invoices = Invoice.objects.filter(customer=obj.customer).order_by('-created_date')
#         invoice_list = []
#         for invoice in invoices:
#             invoice_data = {
#                 'invoice_id': str(invoice.id),
#                 'created_date': serializers.DateTimeField().to_representation(invoice.created_date),
#                 'grand_total': invoice.amout_total,
#                 'reference_no': invoice.reference_no,
#             }
#             invoice_list.append(invoice_data)
#         return invoice_list



# class DashBoardSerializer(serializers.Serializer):
#     total_schedule = serializers.DecimalField(max_digits=10, decimal_places=2)
#     completed_schedule = serializers.DecimalField(max_digits=10, decimal_places=2)
#     coupon_sale = serializers.DecimalField(max_digits=10, decimal_places=2)
#     empty_bottles = serializers.DecimalField(max_digits=10, decimal_places=2)
#     expences = serializers.DecimalField(max_digits=10, decimal_places=2)
#     filled_bottles = serializers.DecimalField(max_digits=10, decimal_places=2)
#     used_coupons = serializers.DecimalField(max_digits=10, decimal_places=2)
#     cash_in_hand = serializers.DecimalField(max_digits=10, decimal_places=2)


class ProdutItemMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProdutItemMaster
        fields = ['id','product_name','unit','tax','rate','created_date']
        
class CustomerSupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerSupply
        fields = ('collected_empty_bottle','created_date')


class CollectionCustomerSerializer(serializers.ModelSerializer):
    invoices = serializers.SerializerMethodField()

    class Meta:
        model = Customers
        fields = ['customer_id','customer_name','invoices']

    def get_invoices(self, obj):
        invoices = Invoice.objects.filter(customer=obj,invoice_status="non_paid",is_deleted=False).order_by('-created_date')
        invoice_list = []
        for invoice in invoices:
            invoice_data = {
                'invoice_id': str(invoice.id),
                'created_date': serializers.DateTimeField().to_representation(invoice.created_date),
                'grand_total': invoice.amout_total,
                'amout_recieved': invoice.amout_recieved,
                'balance_amount': invoice.amout_total - invoice.amout_recieved ,
                'reference_no': invoice.reference_no,
            }
            invoice_list.append(invoice_data)
        return invoice_list
    
class CollectionChequeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionCheque
        fields = ['cheque_amount','cheque_no','bank_name']

class CollectionItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionItems
        fields = '__all__'

class CollectionPaymentSerializer(serializers.ModelSerializer):
    cheque_details = CollectionChequeSerializer(required=False)
    collection_items = CollectionItemsSerializer(many=True, required=False)

    class Meta:
        model = CollectionPayment
        fields = ['payment_method', 'customer', 'amount_received', 'cheque_details', 'collection_items']

    def create(self, validated_data):
        cheque_data = validated_data.pop('cheque_details', None)
        collection_items_data = validated_data.pop('collection_items', None)

        collection_payment = CollectionPayment.objects.create(**validated_data)

        if cheque_data:
            CollectionCheque.objects.create(collection_payment=collection_payment, **cheque_data)

        if collection_items_data:
            for item_data in collection_items_data:
                CollectionItems.objects.create(collection_payment=collection_payment, **item_data)

        return collection_payment
    
class CustodyCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustodyCustom
        fields = ['customer', 'agreement_no', 'deposit_type']
class CustodyCustomItemsSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name.product_name', read_only=True)

    class Meta:
        model = CustodyCustomItems
        fields = ['id', 'custody_custom', 'product', 'product_name', 'quantity', 'serialnumber', 'amount']

# class EmergencyCustomersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DiffBottlesModel
#         fields = '__all__'
class EmergencyCustomersSerializer(serializers.ModelSerializer):
    quantity_required = serializers.IntegerField()
    assign_this_to = serializers.CharField(source='assign_this_to.username', allow_null=True)
    mode = serializers.CharField()
    request_type = serializers.CharField()  # Removed source='request_type'
    delivery_date = serializers.DateTimeField()

    class Meta:
        model = DiffBottlesModel
        fields = ['customer', 'quantity_required', 'assign_this_to', 'mode', 'request_type', 'delivery_date']