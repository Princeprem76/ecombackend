import string
from random import random

from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from order.models import items, orders, coupon
from order.serializers import orderserial, wishSerial
from product.models import products, wishlist
from user.models import UserEmail


def refercode():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))


class cartItem(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            ids = request.query_params.get('id')
            quant = request.query_params.get('quantity')
            size = request.query_params.get('size')
            color = request.query_params.get('color')
            item = get_object_or_404(products, id=ids)
            if item.product_quantity < quant or item.product_quantity == 0:
                return Response({'message': "The product is out of stock!"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                ord, created = items.objects.get_or_create(item=item, user=request.user, current_order=True,
                                                           quantity=quant,
                                                           item_size=size, item_color=color)
                order_qs = orders.objects.filter(order_by=request.user, delivered=False, order_end=False)
                if order_qs.exists():
                    order = order_qs[0]
                    if order.item.filter(item=item).exists():
                        ord.quantity += 1
                        ord.save()
                    else:
                        order.item.add(ord)
                    return Response({'message': "The item is added to cart"}, status=status.HTTP_202_ACCEPTED)
                else:
                    order = orders.objects.create(order_by=request.user)
                    order.item.add(ord)
                    return Response({'message': "The item is added to cart"}, status=status.HTTP_202_ACCEPTED)
        except:
            return Response({'message': 'Parameters are missing'}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request, *args, **kwargs):
        try:
            form = orders.objects.get(order_by__email=request.user, delivered=False, order_end=False)
            serial = orderserial(form, many=False)
            return Response(serial.data, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'No item added to cart!'}, status=status.HTTP_400_BAD_REQUEST)


class remove_single_item_from_cart(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            ids = request.query_params.get('id')
            item = get_object_or_404(products, id=ids)
            order_qs = orders.objects.filter(
                User=request.user,
                orderend=False,
                delivered=False
            )
            if order_qs.exists():
                order = order_qs[0]
                if order.item.filter(items=item).exists():
                    order_item = items.objects.filter(
                        items=item,
                        User=request.user,

                    )[0]
                    if order_item.quantity > 1:
                        order_item.quantity -= 1
                        order_item.save()
                    else:
                        order.item.remove(order_item)

                    return Response({'message': 'The cart is updated.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'You do not have an active order'}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'message': 'Product not found!'}, status=status.HTTP_204_NO_CONTENT)


class wishItem(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            ids = request.query_params.get('id')
            item = get_object_or_404(products, id=ids)
            ord, created = wishlist.objects.get_or_create(product=item, user__email=request.user)
            order_qs = wishlist.objects.get(user__email=request.user)
            if order_qs.exists():
                order = order_qs[0]
                if order.items.filter(product=item).exists():
                    return Response({'message': "Product already added to wishlist"},
                                    status=status.HTTP_208_ALREADY_REPORTED)
                else:
                    order.items.add(ord)
                    return Response({'message': "Product added to wishlist"}, status=status.HTTP_202_ACCEPTED)
            else:
                order = wishlist.objects.create(user__email=request.user)
                order.items.add(ord)
                return Response({'message': "Product added to wishlist"}, status=status.HTTP_202_ACCEPTED)
        except:
            return Response({'message': 'Product not found!'}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request, *args, **kwargs):
        try:
            form = wishlist.objects.get(user__email=request.user)
            serial = wishSerial(form, many=False)
            return Response(serial.data, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'No item in wish list!'}, status=status.HTTP_400_BAD_REQUEST)


class remove_single_item_from_wishlist(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            ids = request.query_params.get('id')
            item = get_object_or_404(products, id=ids)
            order_qs = wishlist.objects.get(
                user__email=request.user,
            )
            if order_qs.exists():
                order = order_qs[0]
                if order.item.filter(product=item).exists():
                    order_item = items.objects.filter(
                        items=item,
                        user__email=request.user,

                    )[0]
                    order.item.remove(order_item)

                    return Response({'message': 'The wishlist is updated!'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'You do not have an active wishlist'}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'message': 'Product not found!'}, status=status.HTTP_204_NO_CONTENT)


class coupon_use(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            ref = data['coupon']
            price = data['price']
            coup = coupon.objects.get(coupon_number=ref)
            newprice = price
            if not coup.is_Expired:
                newprice = price - coup.discount
                dt = {
                    'newprice': newprice,
                    'message': 'The Coupon has been used!'
                }
                return Response(dt, status=status.HTTP_200_OK)
            else:
                dt = {
                    'newprice': newprice,
                    'message': 'The coupon has been expired!'
                }
                return Response(dt, status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response({'message': 'Coupon code does not match'}, status=status.HTTP_400_BAD_REQUEST)
