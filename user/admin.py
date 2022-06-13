from django.contrib import admin
from .models import UserEmail, UserDetails

# Register your models here.
admin.site.register(UserEmail)
admin.site.register(UserDetails)
