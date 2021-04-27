from datetime import datetime, timedelta

from django.conf import settings
from django.db import models

# Create your models here.
from cart.models import Cart
from customer.models import UserProfile, Address
from product.models import Product


class Order(models.Model):
    to_be_delivered = models.DateField(default=datetime.now() + timedelta(days=7))
    user_information = models.ForeignKey(UserProfile, on_delete=models.CASCADE, unique=False)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity = models.PositiveIntegerField()
    total = models.IntegerField(default=0)
    address = models.CharField(max_length=40,default='please enter address')



