from django.urls import path
from . import views

urlpatterns = [
    path('', views.AddToCart.as_view(), name='cart-view'),
    path('mycart/', views.ViewCart.as_view(),name='my-cart'),
]
