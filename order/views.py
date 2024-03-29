import datetime
import string
from random import random, choices
from datetime import date

from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from order.models import items, orders, coupon, location, order_payment
from order.serializers import orderserial, wishSerial, locationSerial, itemSerial
from product.models import products, wishlist, wishitem
from user.models import UserEmail


def refercode():
    return ''.join(choices(string.ascii_lowercase + string.digits, k=8))


def paymentcode():
    return ''.join(choices(string.ascii_lowercase + string.digits, k=10))


class Items(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            ids = request.query_params.get('id')
            quant = request.query_params.get('quantity')
            size = request.query_params.get('size')
            color = request.query_params.get('color')
            item = get_object_or_404(products, id=ids)
            ord, created = items.objects.get_or_create(item=item, item_size=size, item_color=color, user=request.user,
                                          current_order=True)
            ord.quantity += int(quant)
            ord.save()
            return Response({'message': "Successfully added to cart"}, status=status.HTTP_201_CREATED)
        except:
            return Response({'message': "Error"}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request, *args, **kwargs):
        try:
            form = items.objects.filter(user=request.user, current_order=True)
            serial = itemSerial(form, many=True)
            return Response({'item':serial.data}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'No item in cart list!'}, status=status.HTTP_200_OK)


class cartItem(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            itemlist = request.query_params.getlist('ids')
            order_qs = orders.objects.filter(order_by=request.user, delivered=False, order_end=False)
            if order_qs.exists():
                order_qs.delete()
            code = refercode()
            order, creates = orders.objects.get_or_create(order_by=request.user, order_code=code)
            for ord in itemlist:
                order.item.add(ord)
                order.save()

            serial = orderserial(order, many=False)
            return Response({'message': "The item is added to cart", 'Data': serial.data},
                            status=status.HTTP_202_ACCEPTED)
        except:
            return Response({'message': 'Parameters are missing'}, status=status.HTTP_204_NO_CONTENT)


class remove_single_item_from_cart(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            ids = request.query_params.get('id')
            size = request.query_params.get('size')
            color = request.query_params.get('color')
            item = get_object_or_404(products, id=ids)

            order_item = items.objects.filter(
                item=item,
                user=request.user,
                item_size=size, item_color=color,
                current_order=True
            )[0]

            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            return Response({'message': 'The cart is updated.'}, status=status.HTTP_200_OK)

        except:
            return Response({'message': 'Product not found!'}, status=status.HTTP_204_NO_CONTENT)


class remove_whole_item_from_cart(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            ids = request.query_params.get('id')
            size = request.query_params.get('size')
            color = request.query_params.get('color')
            item = get_object_or_404(products, id=ids)
            if items.objects.filter(item=item, item_size=size, item_color=color, current_order=True).exists():
                order_item = items.objects.filter(
                    item=item,
                    user=request.user,
                    current_order=True, item_size=size, item_color=color
                )
                order_item.delete()
                return Response({'message': 'The cart is updated.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No item found'}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'message': 'Product not found!'}, status=status.HTTP_204_NO_CONTENT)


class wishItem(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            ids = request.query_params.get('id')
            item = get_object_or_404(products, id=ids)
            ord, created = wishitem.objects.get_or_create(item=item)
            order_qs = wishlist.objects.filter(user=request.user)
            if order_qs.exists():
                order = order_qs[0]
                if order.product.filter(item=item).exists():
                    return Response({'message': "Product already added to wishlist"},
                                    status=status.HTTP_208_ALREADY_REPORTED)
                else:
                    order.product.add(ord)
                    return Response({'message': "Product added to wishlist"}, status=status.HTTP_202_ACCEPTED)
            else:
                order = wishlist.objects.create(user=request.user)
                order.product.add(ord)
                return Response({'message': "Product added to wishlist"}, status=status.HTTP_202_ACCEPTED)
        except:
            return Response({'message': 'Product not found!'}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request, *args, **kwargs):
        try:
            form = wishlist.objects.filter(user=request.user)
            serial = wishSerial(form, many=True)
            return Response(serial.data, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'No item in wish list!'}, status=status.HTTP_400_BAD_REQUEST)


class remove_single_item_from_wishlist(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            ids = request.query_params.get('id')
            item = get_object_or_404(products, id=ids)
            order_qs = wishlist.objects.filter(
                user=request.user,
            )
            if order_qs.exists():
                order = order_qs[0]
                if order.product.filter(item=item).exists():
                    order_item = wishitem.objects.filter(
                        item=item,
                    )[0]
                    order.product.remove(order_item)

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
            return Response({'message': 'Coupon code does not match'}, status=status.HTTP_204_NO_CONTENT)


class dropLocation(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            email = data['email']
            name = data['name']
            phone = data['phone']
            address = data['address']
            order_qs = orders.objects.get(order_by=request.user, delivered=False, order_end=False)
            ord, created = location.objects.get_or_create(user=request.user, email=email, name=name, phone=int(phone),
                                                          drop_location=address)
            order_qs.drop_location = ord
            order_qs.save()
            return Response({'message': 'Drop Location added'}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Error'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        try:
            loca = location.objects.filter(user=request.user)
            serial = locationSerial(loca, many=True)
            return Response(serial.data, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Error'}, status=status.HTTP_400_BAD_REQUEST)


class Checkout(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            type = data['type']
            payment_method = data['method']
            id = data['payment_id']
            by = data['payment_by']
            price = data['amount']
            order = data['order_code']
            token = data['payment_token']
            pay = True
            if type == 'COD':
                pay = False
                id = paymentcode()
                by = request.user
                token = None
            order_payment(user=request.user, payment_id=id, payment_by=by, amount=int(price), order_code=order,
                          payment_token=token, is_paid=pay, payment_method=payment_method).save()
            order_qs = orders.objects.get(order_by=request.user, delivered=False, order_end=False)
            order_qs.order_end = True
            order_qs.order_date = date.today()
            for i in order_qs.item.all():
                prd = products.objects.get(id=i.item_id)
                prd.product_quantity -= i.quantity
                prd.save()
                it = items.objects.get(user=request.user, id=i.id, current_order=True)
                it.current_order = False
                it.save()
            order_qs.save()
            return Response({'message': 'Payment Done'}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Error'}, status=status.HTTP_400_BAD_REQUEST)
