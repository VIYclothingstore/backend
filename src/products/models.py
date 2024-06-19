from django.db import models

from products.enums import Category, Color, Gender, Size


class Picture(models.Model):
    picture = models.ImageField()
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="images", null=True
    )

    def __str__(self):
        return self.picture.url


class Product(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(
        max_length=15,
        default=Gender.MALE.value,
        choices=Gender.choices(),
    )
    category = models.CharField(
        max_length=15,
        choices=Category.choices(),
    )
    description = models.TextField(max_length=1000, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(
        max_length=15,
        choices=Color.choices(),
    )
    size = models.CharField(
        max_length=15,
        choices=Size.choices(),
    )
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
