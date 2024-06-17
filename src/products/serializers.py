from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category",
            "gender",
            "description",
            "price",
            "available",
            "image_urls",
            "color",
            "size",
        ]
