import math
import logging
from django.shortcuts import redirect
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProductSerializer
from .models import Product
from .mypaginations import ProductPagination
from django.db.models import Q

logger = logging.getLogger(__name__)


class ProductHomePage(APIView):
    queryset = Product.objects.all().order_by('-id')
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

            product_query = Q()
            for i in my_list:
                product_query |= Q(name=i)
            if product_query:
                queryset = queryset.filter(product_query)

        if request.query_params.get('color_values'):
            my_list = request.query_params.get('color_values').split(",")
            my_list = list(map(str.strip, my_list))
            color_query = Q()
            for i in my_list:
                color_query |= Q(color=i)
            if color_query:
                queryset = queryset.filter(color_query)

        if request.query_params.get('size_values'):
            my_list = request.query_params.get('size_values').split(",")
            my_list = list(map(str.strip, my_list))

            size_query = Q()
            for i in my_list:
                size_query |= Q(size=i)
            if size_query:
                queryset = queryset.filter(size_query)

        if request.query_params.get('rating'):
            my_list = request.query_params.get('rating').split(",")
            my_list = list(map(str.strip, my_list))

            rating_query = Q()
            for i in my_list:
                rating_query |= Q(rating=i)
            if rating_query:
                queryset = queryset.filter(rating_query)

        if request.query_params.get('price_less_then'):
            my_list = request.query_params.get('price_less_then').split(",")
            my_list = list(map(str.strip, my_list))

            price_query = Q()
            for i in my_list:
                price_query |= Q(price__lt=i)
            if price_query:
                queryset = queryset.filter(price_query)
        return queryset

    def get(self, request):
        products = self.filter_queryset(request)

        unique_products = self.get_queryset().order_by('name').values_list('name', flat=True).distinct()
        unique_colors = self.get_queryset().order_by('color').values_list('color', flat=True).distinct()
        unique_sizes = self.get_queryset().order_by('size').values_list('size', flat=True).distinct()
        unique_rating = self.get_queryset().order_by('rating').values_list('rating', flat=True).distinct()
        paginator = ProductPagination()
        result = paginator.paginate_queryset(products, request)
        serializer_class = ProductSerializer(result, many=True, context={'request': request})
        total_no_of_products = products.count()
        pages_required = math.ceil(total_no_of_products / paginator.page_size)
        logger.info("Product home page")
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
        logger.info("Page to add product")
        return Response({'serializer': serializer}, template_name='product/addproduct.html')

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return Response({'serializer': serializer})
        serializer.save()
        logger.info("Product added")
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
        logger.info("Product details")
        return Response({'product': self.object})
