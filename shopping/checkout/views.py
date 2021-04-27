import stripe
from datetime import datetime, timedelta

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from card.models import Card
from cart.serializers import AddToCartSerializer
from customer.models import Address
from cart.models import Cart
from customer.serializers import AddressSerializer
from django.conf import settings
from .models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY


class CheckoutPageView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        print(111111111111111)
        cart = Cart.objects.all()
        card = Card.objects.all()
        addresses = Address.objects.all()
        money_to_pay = cart_total()
        total_itema_in_cart = count_products_in_cart()
        address_serializer = AddressSerializer
        return Response({'key': settings.STRIPE_PUBLISHABLE_KEY, 'cart': cart, 'card': card, 'cart_total': money_to_pay,
                         'total_items_in_cart': total_itema_in_cart,
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
        count = count + 1
    return count


class Success(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'checkout/success.html'

    def post(self, request):
        print(request)
        cart = Cart.objects.filter(user=request.user.id)  # Give cart item specific to user
        print(cart)
        # past_order = Order(to_be_delivered=datetime.now() + timedelta(days=7), previous_orders=cart,
        #                                       user_information=request.user)
        try:
            money_to_pay = cart_total()
            charge = stripe.Charge.create(
                amount=money_to_pay * 100,
                currency='inr',
                description='Payment Gateway',
                source=request.POST['stripeToken']
            )
            if cart:
                for data in cart:
                    for product_data in data.product.all():
                        past_order = Order(to_be_delivered=datetime.now() + timedelta(days=7),
                                           user_information=request.user, product=product_data,
                                           quantity=data.quantity, total=data.total, address=data.address)
                        past_order.save()
                cart.delete()

                return Response({'payment_status': "done"})
            else:
                messages.add_message(request, messages.ERROR, 'There are no products in a cart. Please add product for '
                                                              'payment')
                return redirect('/productpage/')
        except IndexError as error:
            raise HttpResponse("There are no products in a cart. Please add product for payment")


class AddAddress(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]

    def post(self, request):
        serializer = AddressSerializer(data=request.data)

        if not serializer.is_valid(raise_exception=False):
            return HttpResponse("Please fill all the fields to save address")
        serializer.save()
        messages.add_message(request, messages.SUCCESS, 'Address Saved Successfully. Now please select the address')
        return redirect('/checkout/')


class PastOrders(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        past_orders = Order.objects.filter(user_information=request.user.id)
        print(past_orders)
        try:
            if past_orders[0].user_information == request.user:
                return Response({'past_orders': past_orders}, template_name='checkout/pastorders.html')
            else:
                messages.add_message(request, messages.WARNING, "you haven't placed any orders")
                return HttpResponse("you haven't placed any orders")
        except IndexError:
            return HttpResponse("There are no orders placed by you")


class UpdateAddress(APIView):

    def put(self, request):
        update_address = request.data
        carts = Cart.objects.filter(user=request.user.id).update(address=update_address['address_detail'])
        return JsonResponse({'msg': 'address updated'}, status=200)

