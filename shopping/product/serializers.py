from .models import Product
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    washable = serializers.ChoiceField(choices=Product.WASHABLE_CHOICES)
    image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Product
        fields = ["id","name", "description", "material", "image", "color", "size",
                  "washable", "discount", "price", "rating"]