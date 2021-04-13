from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.CheckoutPageView.as_view(), name="checkout-page"),
    path('addaddress/', views.AddAddress.as_view(),name='add-address'),
    path('success/', views.Success.as_view(), name='success'),
]
