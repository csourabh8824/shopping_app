from django.urls import path, include
from . import views

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', views.Register.as_view(), name="registration"),
    path('rest-auth/validate/username/', views.ValidateUsername.as_view(), name="validate-username"),
    path('rest-auth/validate/password/', views.ValidateEmail.as_view(), name="validate-email"),
    path('rest-auth/loginview/', views.LoginView.as_view(), name="login"),
    path('accountpage/', views.AccountPage.as_view(), name="account-page"),
    path('productpage/', include('product.urls')),
    path('rest-auth/logoutview/', views.LogoutView.as_view(), name="logout"),
    path('deleteuseraccount/', views.DeleteUserAccount.as_view(), name="deleteuseraccount"),
]
