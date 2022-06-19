from rest_framework import serializers

from order.models import orders, items
from product.models import wishlist
from product.serializers import allProductName


class itemSerial(serializers.ModelSerializer):
    item = allProductName()

    class Meta:
        model = items
        fields = '__all__'


class orderserial(serializers.ModelSerializer):
    item = itemSerial(read_only=True, many=True)

    class Meta:
        model = orders
        fields = '__all__'


class wishSerial(serializers.ModelSerializer):
    product = itemSerial(read_only=True, many=True)

    class Meta:
        model = wishlist
        fields = '__all__'
