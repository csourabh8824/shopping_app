from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from card.models import Card
from customer.models import Address
from cart.models import Cart
from customer.serializers import AddressSerializer
from django.conf import settings


class CheckoutPageView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]

    def get(self,request):
        print(111111111111111)
        cart = Cart.objects.all()
        card = Card.objects.all()
        addresses = Address.objects.all()
        money_to_pay = cart_total()
        total_itema_in_cart = count_products_in_cart()
        address_serializer = AddressSerializer
        return Response({'key': settings.PUBLISHABLE_KEY, 'cart': cart, 'card': card, 'cart_total': money_to_pay, 'total_items_in_cart': total_itema_in_cart,
                         'address_serializer': address_serializer, 'addresses': addresses},
                        status=200,
                        template_name='checkout/checkoutpage.html')



def cart_total():
    total = 0
    cart = Cart.objects.all()
    for products in cart:
        total = total + products.total
    return total


def count_products_in_cart():
    count = 0
    cart = Cart.objects.all()
    for products in cart:
        count = count+1
    return count


class Success(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'checkout/success.html'

    def post(self,request):
        Cart.objects.all().delete()
        return Response({'paymennt_status': "done"})


class AddAddress(APIView):

    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]

    def post(self, request):
        serializer = AddressSerializer(data=request.data)

        if not serializer.is_valid(raise_exception=False):
            return HttpResponse("Please fill all the fields to save address")
        serializer.save()
        messages.add_message(request,messages.SUCCESS, 'Address Saved Successfully Now please select the address')
        return redirect('/checkout/')
