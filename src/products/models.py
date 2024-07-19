from django.core.validators import RegexValidator
from django.db import models
from django.db.models import ManyToManyField

MEN = "Men"
WOMEN = "Women"


class Category(models.Model):
    gender = models.CharField(max_length=10, choices=[(MEN, MEN), (WOMEN, WOMEN)])
    sub_category = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.gender}:{self.sub_category}"


BLACK = "Black"
WHITE = "White"
BLUE = "Blue"
COLORFUL = "Colorful"


class Color(models.Model):
    title = models.CharField(
        max_length=50,
        choices=[(BLACK, BLACK), (WHITE, WHITE), (BLUE, BLUE), (COLORFUL, COLORFUL)],
    )

    def __str__(self):
        return f"{self.title}"


class ProductSize(models.Model):
    value = models.CharField(
        max_length=255, validators=[RegexValidator(regex=r"^[0-9a-zA-Z]+$")]
    )

    def __str__(self):
        return f"{self.value}"


class ProductItem(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="items"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    color = ManyToManyField(Color)
    size = ManyToManyField(ProductSize)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}: {self.category}"


class ProductColor(models.Model):
    product = models.ForeignKey(
        ProductItem, on_delete=models.CASCADE, related_name="colors"
    )
    image = models.ImageField(upload_to="products/")
    color = models.ForeignKey(Color, on_delete=models.CASCADE)


IN_STOCK = "InStock"
SOLD = "Sold"


class WarehouseItem(models.Model):
    product = models.ForeignKey(
        ProductItem, on_delete=models.CASCADE, related_name="wh_items"
    )
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10, choices=[(IN_STOCK, IN_STOCK), (SOLD, SOLD)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.title}:{self.product.category}"
