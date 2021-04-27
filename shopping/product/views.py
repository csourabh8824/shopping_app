import math
from django.shortcuts import render, redirect
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProductSerializer
from .models import Product
from .mypaginations import ProductPagination
from django.db.models import Q


# class ProductHomePage(ListAPIView):
#     queryset = Product.objects.all()
#     renderer_classes = [TemplateHTMLRenderer]
#     serializer_class = ProductSerializer
#     pagination_class = ProductPagination
#     template_name = 'product/productpage.html'
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset().order_by('-id')
#         result = self.pagination_class.paginate_queryset(self, queryset, request)
#         serializer_class = ProductSerializer(result, many=True, context={'request': request})
#
#         total_no_of_products = self.get_queryset().count()
#         print(total_no_of_products)
#         pages_required = math.ceil(total_no_of_products / page_size)
#         return Response({'products': queryset})


class ProductHomePage(APIView):
    queryset = Product.objects.all()
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]

    def get_queryset(self):
        return self.queryset

    def filter_queryset(self, request):
        queryset = self.get_queryset()
        if request.query_params.get('search'):
            queryset = queryset.filter(name__contains=request.query_params.get('search'))
        if request.query_params.get('order_by'):
            queryset = queryset.order_by('-price')
        if request.query_params.get('order_by1'):
            queryset = queryset.order_by('price')
        if request.query_params.get('whats_new'):
            queryset = queryset.all().order_by('-id')

        if request.query_params.get('product_values'):
            my_list = request.query_params.get('product_values').split(",")
            my_list = list(map(str.strip, my_list))
            print(my_list)

            product_query = Q()
            for i in my_list:
                product_query |= Q(name=i)
            print(11,product_query)
            if product_query:
                queryset = queryset.filter(product_query)

        if request.query_params.get('color_values'):
            my_list = request.query_params.get('color_values').split(",")
            my_list = list(map(str.strip, my_list))
            print(my_list)

            color_query = Q()
            for i in my_list:
                color_query |= Q(color=i)
            print(11,color_query)
            if color_query:
                queryset = queryset.filter(color_query)

        if request.query_params.get('size_values'):
            my_list = request.query_params.get('size_values').split(",")
            my_list = list(map(str.strip, my_list))
            print(my_list)

            size_query = Q()
            for i in my_list:
                size_query |= Q(size=i)
            print(11,size_query)
            if size_query:
                queryset = queryset.filter(size_query)

        if request.query_params.get('rating'):
            my_list = request.query_params.get('rating').split(",")
            my_list = list(map(str.strip, my_list))
            print(my_list)

            rating_query = Q()
            for i in my_list:
                rating_query |= Q(rating=i)
            print(11,rating_query)
            if rating_query:
                queryset = queryset.filter(rating_query)

        if request.query_params.get('price_less_then'):
            my_list = request.query_params.get('price_less_then').split(",")
            my_list = list(map(str.strip, my_list))
            print(my_list)

            price_query = Q()
            for i in my_list:
                price_query |= Q(price__lt=i)
            print(11,price_query)
            if price_query:
                queryset = queryset.filter(price_query)
        print(queryset.query)
        return queryset

    def get(self, request):
        products = self.filter_queryset(request)
        # products = Product.objects.order_by('-id')

        unique_products = self.get_queryset().order_by('name').values_list('name', flat=True).distinct()
        unique_colors = self.get_queryset().order_by('color').values_list('color', flat=True).distinct()
        unique_sizes = self.get_queryset().order_by('size').values_list('size', flat=True).distinct()
        unique_rating = self.get_queryset().order_by('rating').values_list('rating', flat=True).distinct()
        paginator = ProductPagination()
        result = paginator.paginate_queryset(products, request)

        serializer_class = ProductSerializer(result, many=True, context={'request': request})

        page_size = 10
        total_no_of_products = products.count()
        pages_required = math.ceil(total_no_of_products / page_size)

        return Response({'serializer': serializer_class.data, 'pages': range(1, pages_required + 1),
                         'unique_products': unique_products, 'unique_colors': unique_colors,
                         'unique_sizes': unique_sizes, 'unique_ratings': unique_rating},
                        template_name='product'
                                      '/productpage.html')


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
