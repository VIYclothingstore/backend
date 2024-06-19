from django.contrib import admin

from .models import Picture, Product


class PictureInline(admin.TabularInline):
    model = Picture
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price", "available"]
    list_filter = ["category", "available"]
    search_fields = ["name"]
    inlines = [PictureInline]
