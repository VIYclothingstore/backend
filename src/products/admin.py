from django.contrib import admin

from .models import Category, Product


@admin.register(Product)
class IssueAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "price"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]
    list_filter = ["name"]
