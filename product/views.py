from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import products, category, subcategory
from product.serializers import allProductName, allCategoryName, subCategoryName, subcategoryAndCategoryName


class allProductView(APIView):
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        try:
            product_data = products.objects.all()
            serializer = allProductName(product_data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'No item available'}, status=status.HTTP_204_NO_CONTENT)


class categoryProductView(APIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            category = data['category']
            product_data = products.objects.filter(product_category__category_name=category)
            serializer = allProductName(product_data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Category not found!'}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request, *args, **kwargs):
        try:
            categoryData = category.objects.all()
            serializer = subcategoryAndCategoryName(categoryData, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'No category present!'}, status=status.HTTP_204_NO_CONTENT)


class subcategoryProductView(APIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            category = data['subcategory']
            product_data = products.objects.filter(sub_category__sub_category_name=category)
            serializer = allProductName(product_data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Category not found!'}, status=status.HTTP_204_NO_CONTENT)

    # def get(self, request, *args, **kwargs):
    #     try:
    #         categoryData = subcategory.objects.all()
    #         serializer = subCategoryName(categoryData, many=True)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     except:
    #         return Response({'message': 'No category present!'}, status=status.HTTP_204_NO_CONTENT)


class singleProductView(APIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        try:
            ids = request.query_params.get('id')
            product_data = products.objects.get(id=ids)
            serializer = allProductName(product_data, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'no data found!'}, status=status.HTTP_204_NO_CONTENT)


class searchProduct(APIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        searched = request.query_params.get('search')
        try:
            qs = products.objects.filter(product_name__icontains=searched)
            qs = qs | products.objects.filter(product_category__category_name__icontains=searched)
            qs = (qs | products.objects.filter(sub_category__sub_category_name__icontains=searched)).distinct()
            serializer = allProductName(qs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'No item found!'}, status=status.HTTP_204_NO_CONTENT)
