from datetime import datetime, timedelta
from django.db import models

# Create your models here.
from cart.models import Cart
from customer.models import UserProfile,Address


class Order(models.Model):
    to_be_delivered = models.DateField(default=datetime.now() + timedelta(days=7))
    previous_orders = models.ForeignKey(Cart, on_delete=models.PROTECT)
    user_information = models.OneToOneField(UserProfile,on_delete=models.CASCADE)
    user_address = models.OneToOneField(Address,on_delete=models.PROTECT)