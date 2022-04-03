from rest_framework import serializers
from .models import *


class AddressInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressInfo
        fields = '__all__'