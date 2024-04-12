from rest_framework import serializers
from .models import Order_change, Order_return, Change_Reason

class OrderChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_change
        fields = '__all__'
    
    

    def update(self, instance, validated_data):
        # Call superclass's update method
        super().update(instance, validated_data)
        return instance

class OrderReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_return
        fields = '__all__'

class ChangeReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Change_Reason
        fields = '__all__'
