from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.ProductHomePage.as_view(), name='product-page'),
    path('addproduct/', views.AddProduct.as_view(), name='add-product'),
    path('productdetail/<int:pk>/', views.ProductDetailView.as_view(), name="product-details"),
    path('addedtocart/', include('cart.urls')),
]

