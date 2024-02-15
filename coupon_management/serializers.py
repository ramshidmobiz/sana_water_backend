from . models import *
from rest_framework import serializers


class couponTypeserializers(serializers.ModelSerializer):

    class Meta :
        model = CouponType
        fields = '__all__'
        
class couponserializers(serializers.ModelSerializer):

    class Meta :
        model = Coupon
        fields = '__all__'

class couponRequestserializers(serializers.ModelSerializer):

    class Meta :
        model = CouponRequest
        fields = '__all__'
        
class assignStaffCouponserializers(serializers.ModelSerializer):

    class Meta :
        model = AssignStaffCoupon
        fields = '__all__'

class assigncustomerCouponserializers(serializers.ModelSerializer):

    class Meta :
        model = AssignStaffCouponDetails
        fields = '__all__'