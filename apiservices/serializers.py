from django.db.models import Sum, Value, DecimalField
from decimal import Decimal
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
from customer_care.models import *

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
    agreement_no = serializers.CharField(source='custody_custom.agreement_no', read_only=True)  
    reference_no = serializers.CharField(source='custody_custom.reference_no', read_only=True)

    class Meta:
        model = CustodyCustomItems
        fields = ['id', 'custody_custom', 'product', 'product_name', 'quantity', 'serialnumber', 'amount', 'deposit_type', 'agreement_no', 'reference_no']

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
                if r.product_item.product_name == "5 Gallon":
                    qty = qty + r.quantity_required
        return qty
    
class SupplyItemProductGetSerializer(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField()

    class Meta:
        model = ProdutItemMaster
        fields = ['id', 'product_name','category','unit','rate','quantity']
        read_only_fields = ['id', 'product_name']

    
    def get_quantity(self, obj):
        customer_id = self.context.get('customer_id')
        qty = 1
        if (reuests:=DiffBottlesModel.objects.filter(delivery_date__date=date.today(), customer__pk=customer_id)).exists():
            for r in reuests :
                if r.product_item.product_name == "5 Gallon":
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
    is_supplied = serializers.SerializerMethodField()
    class Meta:
        model = Customers
        fields = ['customer_id','customer_name','routes','sales_type','products','pending_to_return','coupon_details','is_supplied']
        
    def get_products(self, obj):
        fivegallon = ProdutItemMaster.objects.get(product_name="5 Gallon")
        five_gallon_serializer = SupplyItemFiveGallonWaterGetSerializer(fivegallon, context={"customer_id": obj.pk})
        five_gallon_data = five_gallon_serializer.data
        
        supply_product_data = []
        
        c_requests = DiffBottlesModel.objects.filter(delivery_date__date=date.today(), customer__pk=obj.pk)
        if c_requests.exists():
            for r in c_requests:
                items = ProdutItemMaster.objects.filter(pk=r.product_item.pk)
                if items.exists():
                    supply_product_serializer = SupplyItemProductGetSerializer(items.first(), many=False)
                    supply_product_data.append(supply_product_serializer.data)
        
        return [five_gallon_data] + supply_product_data
    
    def get_pending_to_return(self, obj):
        # total_quantity = CustodyCustomItems.objects.filter(
        #     product__product_name="5 Gallon",
        #     custody_custom__customer=obj
        # ).aggregate(total_quantity=Sum('quantity'))['total_quantity']
        
        total_coupons = CustomerOutstandingReport.objects.filter(customer=obj,product_type="emptycan").aggregate(total=Sum('value', output_field=DecimalField()))['total']
        
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
            coupon_leafs = CouponLeaflet.objects.filter(used=False,coupon__pk__in=list(coupon_ids_queryset)).order_by("leaflet_name")
            leafs = CouponLeafSerializer(coupon_leafs, many=True).data
            
        return {
            'pending_coupons': pending_coupons,
            'digital_coupons': digital_coupons,
            'manual_coupons': manual_coupons,
            'leafs' : leafs,   
        }
        
    def get_is_supplied(self,obj):
        status = False
        if CustomerSupply.objects.filter(customer=obj,created_date__date=datetime.today().date()).exists() :
            status = True
        return status

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
    product_rate = serializers.SerializerMethodField()
    class Meta:
        model = VanProductStock
        fields = '__all__'
        
    def get_product_name(self, obj):
        return obj.product.product_name
    
    def get_product_rate(self, obj):
        return obj.product.rate
    






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
        invoices = Invoice.objects.filter(customer=obj,invoice_status="non_paid",is_deleted=False).exclude(amout_total__lt=1).order_by('-created_date')
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
            if not invoice.amout_total == invoice.amout_recieved:
                invoice_list.append(invoice_data)
            else:
                invoice.invoice_status="paid"
                invoice.save()
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
    
# class CustodyCustomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustodyCustom
#         fields = ['customer', 'agreement_no', 'deposit_type','reference_no']
# class CustodyCustomItemsSerializer(serializers.ModelSerializer):
#     product_name = serializers.CharField(source='product.product_name.product_name', read_only=True)
#     deposit_type = serializers.CharField(source='custody_custom.deposit_type', read_only=True)
#     agreement_no = serializers.CharField(source='custody_custom.agreement_no', read_only=True)  
#     reference_no = serializers.CharField(source='custody_custom.reference_no', read_only=True)

#     class Meta:
#         model = CustodyCustomItems
#         fields = ['id', 'custody_custom', 'product', 'product_name', 'quantity', 'serialnumber', 'amount','reference_no','agreement_no','deposit_type']
class CustomerCustodyStockProductsSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField() 
    deposit_form_number = serializers.SerializerMethodField() 
    amount = serializers.SerializerMethodField() 

    class Meta:
        model = CustomerCustodyStock
        fields = ['agreement_no','deposit_type','product','product_name','quantity','serialnumber','amount','deposit_form_number']
        
    def get_product_name(self,obj):
        return obj.product.product_name
    
    def get_deposit_form_number(self,obj):
        return ""
    
    def get_amount(self,obj):
        return int(obj.amount)

class CustomerCustodyStockSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField() 
    customer = serializers.SerializerMethodField() 

    class Meta:
        model = Customers
        fields = ['customer_id','customer','customer_name','products']
        
    def get_products(self,obj):
        instances = CustomerCustodyStock.objects.filter(customer=obj)
        return CustomerCustodyStockProductsSerializer(instances,many=True).data
    
    def get_customer(self,obj):
        return obj.customer_name
    

class CustodyCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustodyCustom
        fields = ['customer', 'agreement_no', 'deposit_type', 'reference_no']

class CustodyCustomItemsSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name.product_name', read_only=True)
    deposit_type = serializers.CharField(source='custody_custom.deposit_type', read_only=True)
    agreement_no = serializers.CharField(source='custody_custom.agreement_no', read_only=True)  
    reference_no = serializers.CharField(source='custody_custom.reference_no', read_only=True)

    class Meta:
        model = CustodyCustomItems
        fields = ['id', 'custody_custom', 'product', 'product_name', 'quantity', 'serialnumber', 'amount', 'reference_no', 'agreement_no', 'deposit_type']
        
# class EmergencyCustomersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DiffBottlesModel
#         fields = '__all__'
class EmergencyCustomersSerializer(serializers.ModelSerializer):
    quantity_required = serializers.IntegerField()
    assign_this_to = serializers.CharField(source='assign_this_to.username', allow_null=True)
    mode = serializers.CharField()
    delivery_date = serializers.DateTimeField()

    class Meta:
        model = DiffBottlesModel
        fields = ['customer', 'quantity_required', 'assign_this_to', 'mode', 'product_item', 'delivery_date']


#----------------------New sales Report-------------

class NewSalesCustomerSupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerSupply
        fields = '__all__'

class NewSalesCustomerCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerCoupon
        fields = '__all__'

class NewSalesCollectionPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionPayment
        fields = '__all__'
        
        
class CustomerCustodySerializer(serializers.Serializer):
    customer = serializers.SerializerMethodField() 
    agreement_no = serializers.SerializerMethodField() 
    total_amount = serializers.SerializerMethodField() 
    deposit_type = serializers.SerializerMethodField() 
    reference_no = serializers.SerializerMethodField() 
    product = serializers.SerializerMethodField() 
    quantity = serializers.SerializerMethodField() 
    serialnumber = serializers.SerializerMethodField() 



class CreditNoteSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()

   
    class Meta:
        model = Invoice
        fields = ['id','customer','customer_name', 'invoice_no', 'invoice_type','invoice_status','amout_total', 'amout_recieved']

    def get_customer_name(self, obj):
        return obj.customer.customer_name
    
class CollectionReportSerializer(serializers.ModelSerializer):
    customer_id = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField()
    receipt_no = serializers.CharField(source='invoice.reference_no')
    mode_of_payment = serializers.CharField(source='collection_payment.payment_method')
    collected_amount = serializers.DecimalField(source='amount_received', max_digits=10, decimal_places=2)

    class Meta:
        model = CollectionItems
        fields = ['customer_id', 'customer_name', 'receipt_no', 'mode_of_payment', 'collected_amount']

    def get_customer_id(self, obj):
        return obj.collection_payment.customer.customer_id

    def get_customer_name(self, obj):
        return obj.collection_payment.customer.customer_name

class CouponSupplyCountSerializer(serializers.ModelSerializer):
    customer__customer_name = serializers.CharField()  
    manual_coupon_paid_count = serializers.IntegerField()
    manual_coupon_free_count = serializers.IntegerField()
    digital_coupon_paid_count = serializers.IntegerField()
    digital_coupon_free_count = serializers.IntegerField()
    total_amount_collected = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_type = serializers.ChoiceField(choices=PAYMENT_METHOD)  # Use ChoiceField for dropdown with choices

    class Meta:
        model = CustomerCoupon
        fields = ['customer__customer_name', 'manual_coupon_paid_count', 'manual_coupon_free_count', 'digital_coupon_paid_count', 'digital_coupon_free_count', 'total_amount_collected', 'payment_type']


class CustomerCouponCountsSerializer(serializers.Serializer):
    customer_name = serializers.CharField()
    building_name = serializers.CharField()
    digital_coupons_count = serializers.IntegerField()
    manual_coupons_count = serializers.IntegerField()

    
    
# class StockMovementReportSerializer(serializers.ModelSerializer):
#     customer_name = serializers.SerializerMethodField()
#     product_name = serializers.SerializerMethodField()
   
#     class Meta:
#         model = CustomerSupplyItems
#         fields = [ 'product', 'quantity','customer_name','product_name']
        
#     def get_customer_name(self, obj):
#         return obj.customer_supply.customer.customer_name  
#     def get_product_name(self, obj):
#         return obj.product.product_name 

class CustomerSupplySerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomerSupply
        fields = '__all__'

class CustomersStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = ['customer_id','customer_name','building_name','door_house_no','floor_no','customer_type','sales_type']

class CustomerOutstandingAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutstandingAmount
        fields = '__all__'

class OutstandingSerializer(serializers.ModelSerializer):
    outstandingamount_set = serializers.SerializerMethodField()

    class Meta:
        model = CustomerOutstanding
        fields = '__all__'
        
    def get_outstandingamount_set(self, obj):
        instances = OutstandingAmount.objects.filter(customer_outstanding__pk=obj.pk)
        return CustomerOutstandingAmountSerializer(instances, many=True).data
    
class SalesmanExpensesSerializer(serializers.ModelSerializer):
    head_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Expense
        fields = ['head_name','amount']
    
    def get_head_name(self,obj):
        return obj.expence_type.name
    
class CashSaleSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    building_name = serializers.SerializerMethodField()
    class Meta:
        model = Invoice
        fields = ['reference_no','customer_name','building_name','net_taxable','vat','amout_total']
    
    def get_customer_name(self, obj):
        return obj.customer.customer_name
    def get_building_name(self, obj):
        return obj.customer.building_name            
    
class CreditSaleSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    building_name = serializers.SerializerMethodField()
    class Meta:
        model = Invoice
        fields = ['reference_no','customer_name','building_name','net_taxable','vat','amout_total']
    
    def get_customer_name(self, obj):
        return obj.customer.customer_name
    def get_building_name(self, obj):
        return obj.customer.building_name
    
class SalesmanRequestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SalesmanRequest
        fields = ['request']
        
class CompetitorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competitors
        fields = '__all__' 
             
class MarketShareSerializers(serializers.ModelSerializer):
    class Meta :
        model = MarketShare
        fields = ['product','customer','competitor','quantity','price']
        
class OffloadVanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offload
        fields = ['id', 'created_by', 'created_date', 'modified_by', 'modified_date', 'van', 'product', 'quantity', 'stock_type']
        
        
        
class CustomerSupplySerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Customers
        fields = ['customer_name','mobile_no','building_name','door_house_no','floor_no']



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProdutItemMaster
        fields = '__all__'

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name', 'quantity']


class CustodyCustomItemsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CustodyCustomItems
        fields = '__all__'

class CustodyCustomSerializer(serializers.ModelSerializer):
    custody_custom_items = CustodyCustomItemsSerializer(many=True, source='custodycustomitems_set')

    class Meta:
        model = CustodyCustom
        fields = '__all__'

class VanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Van
        fields = ['van_id', 'van_make', 'plate', 'capacity']

class VanProductStockSerializer(serializers.ModelSerializer):
    van = VanSerializer(read_only=True)
    
    class Meta:
        model = VanProductStock
        fields = ['id', 'product', 'stock_type', 'count', 'van']




class VanProductSerializer(serializers.ModelSerializer):
    van = VanSerializer()
    product = serializers.StringRelatedField()

    class Meta:
        model = VanProductStock
        fields = ['id', 'product', 'stock_type', 'count', 'van']

class VanCouponStockSerializer(serializers.ModelSerializer):
    van = VanSerializer()
    coupon = serializers.StringRelatedField()

    class Meta:
        model = VanCouponStock
        fields = ['id', 'coupon', 'stock_type', 'count', 'van']


class CouponConsumptionSerializer(serializers.Serializer):
    customer__customer_name = serializers.CharField()
    total_digital_leaflets = serializers.IntegerField()
    total_manual_leaflets = serializers.IntegerField()

class FreshCanStockSerializer(serializers.ModelSerializer):
    van = VanSerializer(read_only=True)
    
    class Meta:
        model = VanProductStock
        fields = ['id', 'product', 'stock_type', 'count', 'van']
class ManualCustomerCouponSerializer(serializers.ModelSerializer):
    van = CouponConsumptionSerializer(read_only=True)
    
    class Meta:
        model = CustomerCoupon
        fields = ['id', 'amount_recieved', 'coupon_method']

class DigitalCouponSerializer(serializers.ModelSerializer):
    van = CouponConsumptionSerializer(read_only=True)
    
    class Meta:
        model = CustomerSupplyDigitalCoupon
        fields = ['id', 'count']

class FreshCanStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = VanProductStock
        fields = ['count']

class FreshvsCouponCustomerSerializer(serializers.ModelSerializer):
    fresh_cans = serializers.SerializerMethodField()
    total_digital_coupons = serializers.SerializerMethodField()
    total_manual_coupons = serializers.SerializerMethodField()
    opening_cans = serializers.SerializerMethodField()  
    pending_cans = serializers.SerializerMethodField()

    class Meta:
        model = Customers
        fields = ['customer_name', 'customer_type', 'fresh_cans', 'total_digital_coupons', 'total_manual_coupons', 'opening_cans','pending_cans']

    def get_fresh_cans(self, obj):
        request = self.context.get('request')
        start_datetime = request.data.get('start_date')
        end_datetime = request.data.get('end_date')

        fresh_cans = Staff_IssueOrders.objects.filter(
            salesman_id=obj.sales_staff,
            # created_date__range=[start_datetime, end_datetime],
            status='Order Issued'
        ).aggregate(total_fresh_cans=Sum('quantity_issued'))
        print("fresh_cans", fresh_cans)

        return fresh_cans.get('total_fresh_cans', 0) or 0

    def get_total_digital_coupons(self, obj):
        request = self.context.get('request')
        start_datetime = request.data.get('start_date')
        end_datetime = request.data.get('end_date')

        digital_coupon_data = CustomerSupplyDigitalCoupon.objects.filter(
            customer_supply__customer=obj,
            customer_supply__created_date__range=[start_datetime, end_datetime]
        ).aggregate(total_digital_leaflets=Sum('count'))
        print("digital_coupon_data", digital_coupon_data)
        return digital_coupon_data.get('total_digital_leaflets', 0) or 0

    def get_total_manual_coupons(self, obj):
        request = self.context.get('request')
        start_datetime = request.data.get('start_date')
        end_datetime = request.data.get('end_date')

        manual_coupon_data = CustomerCouponItems.objects.filter(
            customer_coupon__customer=obj,
            customer_coupon__created_date__range=[start_datetime, end_datetime],
            coupon__coupon_method='manual',
            coupon__leaflets__used=False
        ).aggregate(total_manual_leaflets=Count('coupon__leaflets', distinct=True))
        print("manual_coupon_data", manual_coupon_data)
        return manual_coupon_data.get('total_manual_leaflets', 0) or 0

    def get_opening_cans(self, obj):
        request = self.context.get('request')
        start_datetime = request.data.get('start_date')
        end_datetime = request.data.get('end_date')
        
        opening_cans = VanProductStock.objects.filter(
            van__salesman=obj.sales_staff,
            stock_type='opening_stock',
            van__created_date__range=[start_datetime, end_datetime]
        ).aggregate(total_opening_cans=Sum('count'))
        print("opening_cans", opening_cans)
        
        return opening_cans.get('total_fresh_cans', 0) or 0
    
    def get_pending_cans(self, obj):
        request = self.context.get('request')
        start_datetime = request.data.get('start_date')
        end_datetime = request.data.get('end_date')
        
        pending_cans = Staff_Orders_details.objects.filter(
            # staff_order_id__salesman_id=obj.sales_staff,
            status='Pending',
            created_date__range=[start_datetime, end_datetime]
        ).aggregate(total_pending_cans=Sum('count'))
        print("pending_cans", pending_cans)
        
        return pending_cans.get('total_pending_cans', 0) or 0

class CustomerOrdersSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomerOrders
        fields = ('id','product','quantity','total_amount','no_empty_bottle_return','empty_bottle_required','no_empty_bottle_required','empty_bottle_amount','total_net_amount','delivery_date','payment_option','order_status')
        read_only_fields = ('id','order_status')
        
class CustomerOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerOrders
        fields = ['id', 'product', 'order_status', 'delivery_date']





class CustomerCouponPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerOrders
        fields = ['id', 'created_date', 'order_status']

class CustomerOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer_Order
        fields = ['order_number', 'created_date', 'payment_option']

class StockMovementProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovementProducts
        fields = ['id', 'product', 'quantity']

class StockMovementSerializer(serializers.ModelSerializer):
    products = StockMovementProductsSerializer(many=True, write_only=True)

    class Meta:
        model = StockMovement
        fields = ['id', 'created_by', 'salesman', 'from_van', 'to_van', 'products']

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        stock_movement = StockMovement.objects.create(**validated_data)
        
        for product_data in products_data:
            StockMovementProducts.objects.create(stock_movement=stock_movement, **product_data)

            # Update stock for from_van
            from_van_product = VanProductStock.objects.get(van=stock_movement.from_van, product=product_data['product'])
            from_van_product.count -= product_data['quantity']
            from_van_product.save()

            # Update stock for to_van
            to_van_product, created = VanProductStock.objects.get_or_create(van=stock_movement.to_van, product=product_data['product'])
            to_van_product.count += product_data['quantity']
            to_van_product.save()
        
        return stock_movement
    
    
class NonVisitReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = NonVisitReason
        fields = ['reason_text']
        
        
class CustomerComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerComplaint
        fields = '__all__'