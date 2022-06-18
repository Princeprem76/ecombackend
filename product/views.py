from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import products, category
from product.serializers import allProductName, allCategoryName


class allProductView(APIView):
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        try:
            product_data = products.objects.all()
            serializer = allProductName(product_data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'message':'No item available'}, status=status.HTTP_204_NO_CONTENT)


class categoryProductView(APIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        data = request.data
        category = data['category']
        product_data = products.objects.filter(product_category__category_name=category)
        serializer = allProductName(product_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        categoryData = category.objects.all()
        serializer = allCategoryName(categoryData, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class singleProductView(APIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        try:
            ids= request.query_params.get('id')
            product_data = products.objects.get(id=ids)
            serializer = allProductName(product_data, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'message':'no data found!'}, status=status.HTTP_400_BAD_REQUEST)


