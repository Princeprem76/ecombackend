from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import UserEmail


class UserhasDataSerial(serializers.ModelSerializer):
    class Meta:
        model = UserEmail
        fields = ['is_verified', 'has_data', 'is_user']
