from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from product.models import products
from product.serializers import allProductView


@api_view(['GET'])
def allProductView(request):
    product_data = products.objects.all()
    serializer = allProductView(product_data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def categoryProductView(request, pk):
    product_data = products.objects.filter(product_category__category_name=pk)
    serializer = allProductView(product_data, many=True)
    return Response(serializer.data)
