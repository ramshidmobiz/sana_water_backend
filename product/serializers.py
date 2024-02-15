from . models import Product,Product_Default_Price_Level
from rest_framework import serializers


class ProductSerializers(serializers.ModelSerializer):
    class Meta :
        model = Product
        fields = '__all__'


class Product_Default_Price_Level_Serializers(serializers.ModelSerializer):
    class Meta :
        model = Product_Default_Price_Level
        fields = '__all__'

