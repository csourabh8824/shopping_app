from django.contrib import admin
from .models import UserProfile, Address

# Register your models here.


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["id","username", "email", "first_name", "last_name", "password", "mobile_number",
                    "alternate_mobile_number", "gender", "birthdate"]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["id", "country", "state", "city", "pincode", "street_number", "permanent_address",
                  "type_of_address", "user"]