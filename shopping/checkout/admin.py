from django.contrib import admin
from .models import Order
# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'to_be_delivered', 'user_information', 'product', 'quantity', 'total', 'address']
