from django.contrib import admin

from .models import Product


@admin.register(Product)
class IssueAdmin(admin.ModelAdmin):

    list_display = ["id", "name", "price"]
