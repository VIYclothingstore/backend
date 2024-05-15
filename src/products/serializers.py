from rest_framework import serializers

from .models import ProductCategory, Color, Product


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('id', 'name', 'value')


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('id', 'name', 'description')


class ProductSerializer(serializers.ModelSerializer):
    available_color = ColorSerializer(many=True, read_only=True)
    category = ProductCategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'price',
            'image',
            'available_color',
            'category',
            'is_for_women',
            'is_for_men',
        )
