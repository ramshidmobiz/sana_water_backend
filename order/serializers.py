from rest_framework import serializers
from .models import Order_change, Order_return, Change_Reason

class ChangeReasonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Change_Reason
        fields = ['reason_name']
        
class OrderChangeSerializer(serializers.ModelSerializer):
    reason = ChangeReasonsSerializer(read_only=True)
    reason_id = serializers.PrimaryKeyRelatedField(
        queryset=Change_Reason.objects.all(), write_only=True, source='reason'
    )

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
