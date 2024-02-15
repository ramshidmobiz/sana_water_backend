from rest_framework import serializers
from . models import *

class CustomUserSerializers(serializers.ModelSerializer):
    class Meta :
        model = CustomUser
        exclude = ['groups','user_permissions']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class CustomersSerializers(serializers.ModelSerializer):
    class Meta :
        model = Customers
        fields = '__all__'

class Create_Customers_Serializers(serializers.ModelSerializer):
    class Meta :
        model = Customers
        fields = '__all__'