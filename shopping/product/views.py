from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.generics import RetrieveAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProductSerializer
from .models import Product


class ProductHomePage(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        products = Product.objects.all()
        for data in products:
            print(data.image.url)

        return Response({'products': products}, template_name='product/productpage.html')


class AddProduct(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'product/addproduct.html'
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        serializer = ProductSerializer
        return Response({'serializer': serializer}, template_name='product/addproduct.html')

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return Response({'serializer': serializer})
        serializer.save()
        return redirect('/productpage/')
        # return Response({'msg': 'Product added'}, status=200)


class ProductDetailView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'product/productdetail.html'

    def retrieve(self, request, *args, **kwargs):

        self.object = self.get_object()
        serializer = self.get_serializer(self.object)
        # return Response(serializer.data)
        return Response({'product': self.object})

