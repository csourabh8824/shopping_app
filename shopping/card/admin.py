from django.contrib import admin
from .models import Card
# Register your models here.


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display =["id", "name_on_card", "card_type", "expiration","card_user"]

