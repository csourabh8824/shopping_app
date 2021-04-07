from django.contrib import admin
from .models import Cart


# Register your models here.

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display =["id","user", "get_products" ,"total", "quantity"]
    raw_id_fields = ["product"]
