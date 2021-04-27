from rest_framework import serializers
from .models import Cart


class AddToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["user", "product", "total", "quantity"]
