from rest_framework import serializers

from order.models import orders
from product.models import wishlist


class orderserial(serializers.ModelSerializer):
    class Meta:
        model = orders
        fields = '__all__'


class wishSerial(serializers.ModelSerializer):
    class Meta:
        model: wishlist
        fields = '__all__'
