from django.db import models
from customer.models import UserProfile, Address
from product.models import Product


class Cart(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, unique=False)
    product = models.ManyToManyField(Product)
    total = models.IntegerField(default=0)
    # updated = models.DateTimeField(auto_now=True)
    quantity = models.PositiveIntegerField()
    address = models.CharField(max_length=40,default='please add address',)

    def get_products(self):
        return ",".join([str(p) for p in self.product.all()])
