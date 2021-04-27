from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from .models import Cart
from .serializers import AddToCartSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from product.models import Product


class ViewCart(ListAPIView):
    queryset = Cart.objects.all()
    # serializer_class = AddToCartSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'cart/cartpage.html'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        for data in queryset:
            print(data.id)
        return Response({'cart': queryset,'logged_in_user':request.user})


class AddToCart(APIView):

    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]

    def post(self, request, format=None):

        p_id = request.data['product_id']
        product = Product.objects.get(id=p_id)

        request.data['user'] = request.user.id
        request.data['product'] = [product.id]
        price = product.price
        request.data['total'] = int(request.data['quantity'])*price

        print(2222222222222222222222222222222222222222222,request.data)
        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print(111111111111111, serializer.validated_data)
            serializer.save()
            return JsonResponse({'msg': serializer.data},status=200)


class UpdateCart(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]

    def put(self,request,*args, **kwargs):
        update_data = request.data
        print(update_data)

        cart_data = Cart.objects.get(pk=request.data['id'])

        for product_data in cart_data.product.all():
            update_data['total'] = product_data.price*int(update_data['quantity'])

        serializer = AddToCartSerializer(cart_data, data=update_data, partial=True)
        serializer.is_valid(raise_exception=True)
        print(22222222222, serializer.validated_data)
        serializer.save()
        return JsonResponse({'msg': 'Data Updated!!'}, status=200)


class DeleteCartItem(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, pk=None):
        data = request.data
        Cart.objects.get(pk=pk).delete()
        print(7777777777777)
        return redirect('/productpage/')


