from django.db import models
from customer.models import UserProfile
from product.models import Product


class Cart(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,unique=False)
    product = models.ManyToManyField(Product)
    total = models.IntegerField(default=0)
    # updated = models.DateTimeField(auto_now=True)
    quantity = models.PositiveIntegerField()

    def get_products(self):
        return ",".join([str(p) for p in self.product.all()])