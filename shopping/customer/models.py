from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    USERNAME_FIELD = "username"
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=120, null=True)
    mobile_number = models.IntegerField(null=True)
    alternate_mobile_number = models.IntegerField(null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    birthdate = models.DateField(blank=True, null=True)


class Address(models.Model):
    ADDRESS_CHOICES = [
        ('HOME', 'Home'),
        ('OFFICE', 'Office'),
    ]
    COUNTRY_CHOICES = [
        ('INDIA', 'India'),
        ('AUSTRALIA', 'Australia'),
        ('ENGLAND', 'England'),
    ]
    country = models.CharField(max_length=15, choices=COUNTRY_CHOICES)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=15)
    pincode = models.IntegerField()
    street_number = models.IntegerField()
    permanent_address = models.CharField(max_length=50)
    type_of_address = models.CharField(max_length=10, choices=ADDRESS_CHOICES)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


