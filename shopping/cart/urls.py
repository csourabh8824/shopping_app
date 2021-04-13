from django.urls import path
from . import views

urlpatterns = [
    path('', views.AddToCart.as_view(), name='cart-view'),
    path('mycart/', views.ViewCart.as_view(), name='my-cart'),
    path('deletedcartitem/<int:pk>/', views.DeleteCartItem.as_view(), name='delete-cart-item'),
    path('updatecart/', views.UpdateCart.as_view(), name='update-cart'),
]
