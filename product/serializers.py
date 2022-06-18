from rest_framework import serializers

from product.models import products, category, subcategory


class subCategoryName(serializers.ModelSerializer):
    class Meta:
        model = subcategory
        fields = ['sub_category_name']


class allCategoryName(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = ['id', 'category_name', 'sub_category']


class allProductName(serializers.ModelSerializer):
    product_category = allCategoryName()
    class Meta:
        model = products
        fields = ['id', 'product_name', 'product_image', 'product_price', 'product_category', 'get_discounted_price',
                  'product_discount', 'is_top_selling']
