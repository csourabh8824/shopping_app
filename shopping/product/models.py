from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# from customer.models import UserProfile


class Product(models.Model):
    WASHABLE_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, default="Awesome Product")
    material = models.CharField(max_length=30)
    image = models.ImageField(default='default.jpg',upload_to='product_images')
    color = models.CharField(max_length=10)
    size = models.CharField(max_length=10)
    washable = models.CharField(max_length=5, choices=WASHABLE_CHOICES)
    discount = models.IntegerField()
    price = models.PositiveIntegerField()
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)])

