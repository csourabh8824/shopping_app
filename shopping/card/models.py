from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.
from customer.models import UserProfile


class Card(models.Model):

    CARD_TYPE = [
        ('CREDIT CARD', 'Credit card'),
        ('DEBIT CARD', 'Debit card'),
    ]

    name_on_card = models.CharField(max_length=20)
    card_type = models.CharField(max_length=20,choices=CARD_TYPE)
    expiration = models.CharField(max_length=10)
    card_user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
