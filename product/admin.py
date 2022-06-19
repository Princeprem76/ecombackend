from django.contrib import admin
from .models import subcategory, category, products, wishlist, productImage, productColor, productSize

# Register your models here.
admin.site.register(subcategory)
admin.site.register(category)
admin.site.register(products)
admin.site.register(wishlist)
admin.site.register(productImage)
admin.site.register(productColor)
admin.site.register(productSize)