from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=100)


class Color(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField()


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    available_color = models.ManyToManyField(Color, blank=True)
    category = models.ManyToManyField(ProductCategory, related_name='products', ),
    is_for_women = models.BooleanField(default=False)
    is_for_men = models.BooleanField(default=False)


class WarehouseItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.IntegerField()
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=False)
