from django.contrib import admin
from .models import subcategory, category, products, wishlist

# Register your models here.
admin.site.register(subcategory)
admin.site.register(category)
admin.site.register(products)
admin.site.register(wishlist)
