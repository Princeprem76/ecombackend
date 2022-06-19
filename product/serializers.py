from rest_framework import serializers

from product.models import products, category, subcategory, productImage


class subCategoryName(serializers.ModelSerializer):
    class Meta:
        model = subcategory
        fields = '__all__'


class allCategoryName(serializers.ModelSerializer):
    sub_category = subCategoryName(read_only=True, many=True)

    class Meta:
        model = category
        fields = ['id', 'category_name', 'sub_category']


class allImages(serializers.ModelSerializer):
    class Meta:
        model = productImage
        fields = ['product_image']


class allProductName(serializers.ModelSerializer):
    product_category = allCategoryName()
    product_image = allImages(read_only=True, many=True)

    class Meta:
        model = products
        fields = ['id', 'product_name', 'product_quantity', 'product_image', 'product_price', 'product_category',
                  'get_discounted_price',
                  'product_discount', 'is_top_selling', 'get_image_count']
