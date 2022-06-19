from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import UserEmail


class UserhasDataSerial(serializers.ModelSerializer):
    class Meta:
        model = UserEmail
        fields = ['is_verified', 'is_user']


class UserData(serializers.ModelSerializer):
    class Meta:
        model = UserEmail
        fields = ['name', 'get_image', 'phone', 'get_gender', 'address']


class UserProfile(serializers.ModelSerializer):
    class Meta:
        model = UserEmail
        fields = ['name', 'get_image']
