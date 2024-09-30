# Register your models here.
from django.contrib import admin

from order.models import Basket, BasketItem


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "updated_at")
    list_filter = ("user",)
    date_hierarchy = "created_at"
    search_fields = ("id", "user")


@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = ("basket", "product", "color", "size", "quantity", "created_at")
    list_filter = ("basket", "product", "color", "size", "quantity")
    date_hierarchy = "created_at"
    search_fields = ("basket", "product", "color", "size", "quantity")
