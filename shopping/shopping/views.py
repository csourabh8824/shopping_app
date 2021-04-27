from django.shortcuts import render
from django.views import View
from product.models import Product

class HomeView(View):

    def get(self, request):
        return render(request, 'base.html')
