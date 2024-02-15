from . models import *
from rest_framework import serializers



class VanSerializers(serializers.ModelSerializer):
    class Meta :
        model = Van
        fields = '__all__'


class VanRoutesSerializers(serializers.ModelSerializer):
    class Meta :
        model = Van_Routes
        fields = '__all__'


class Van_LicenseSerializers(serializers.ModelSerializer):
    class Meta :
        model = Van_License
        fields = '__all__'