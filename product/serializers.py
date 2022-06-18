from rest_framework import serializers

from product.models import products, category, subcategory


class allProductName(serializers.ModelSerializer):
    class Meta:
        model = products
        fields = ['id', 'product_name', 'product_image', 'product_price', 'product_category', 'get_discounted_price',
                  'product_discount', 'is_top_selling']


class subCategoryName(serializers.ModelSerializer):
    class Meta:
        model = subcategory
        fields = '__all__'


class allCategoryName(serializers.ModelSerializer):
    sub_category = subCategoryName

    class Meta:
        model = category
        fields = ['id', 'category_name', 'sub_category']
