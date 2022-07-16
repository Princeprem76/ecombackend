from rest_framework import serializers

from product.models import products, category, subcategory, productImage, productColor, productSize


class subCategoryName(serializers.ModelSerializer):
    class Meta:
        model = subcategory
        fields = ['sub_category_name']


class allCategoryName(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = ['category_name']


class subcategoryAndCategoryName(serializers.ModelSerializer):
    sub_category = subCategoryName(read_only=True, many=True)

    class Meta:
        model = category
        fields = ['category_name', 'sub_category']


class allImages(serializers.ModelSerializer):
    class Meta:
        model = productImage
        fields = ['product_image']


class allSize(serializers.ModelSerializer):
    class Meta:
        model = productSize
        fields = ['product_size']


class allColor(serializers.ModelSerializer):
    class Meta:
        model = productColor
        fields = ['product_color']


class allProductName(serializers.ModelSerializer):
    sub_category = subCategoryName()
    product_category = allCategoryName()
    product_image = allImages(read_only=True, many=True)
    product_size = allSize(read_only=True, many=True)
    product_color = allColor(read_only=True, many=True)

    class Meta:
        model = products
        fields = ['id', 'product_name', 'product_quantity', 'product_image', 'product_price', 'product_category',
                  'sub_category',
                  'get_discounted_price',
                  'product_discount', 'is_top_selling', 'get_image_count', 'product_size', 'product_color',
                  'product_description']
