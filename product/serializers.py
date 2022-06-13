from rest_framework import serializers

from product.models import products


class allProductView(serializers.ModelSerializer):
    class Meta:
        model = products
        fields = ['product_name', 'product_image', 'product_price', 'product_category', 'get_discounted_price',
                  'product_discount']
