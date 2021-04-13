from django.urls import path
from . import views

urlpatterns = [
    path('', views.AddCard.as_view(), name='card-view'),

]
