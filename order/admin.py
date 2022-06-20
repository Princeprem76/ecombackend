from django.contrib import admin
from .models import orders, items, order_payment,location

# Register your models here.
admin.site.register(items)
admin.site.register(orders)
admin.site.register(order_payment)
admin.site.register(location)
