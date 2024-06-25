from rest_framework import serializers

from .models import (
    IN_STOCK,
    Category,
    Color,
    ProductImage,
    ProductItem,
    ProductSize,
    WarehouseItem,
)


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ["image_url"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.image.url)


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = "__all__"


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(
        many=True,
        read_only=True,
    )
    color = ColorSerializer(read_only=True, many=True)
    size = ProductSizeSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True, many=False)

    quantity = serializers.SerializerMethodField(
        "get_quantity",
        read_only=True,
    )

    def get_quantity(self, obj):
        return obj.wh_items.filter(status=IN_STOCK).count()

    class Meta:
        model = ProductItem
        fields = [
            "id",
            "title",
            "category",
            "description",
            "price",
            "color",
            "size",
            "images",
            "quantity",
        ]


class WarehouseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseItem
        fields = "__all__"
