from django.contrib import admin

from .models import Product, ProductCategory

admin.site.register(Product)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(ProductCategory)


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
