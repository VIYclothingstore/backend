from rest_framework import serializers

from .models import (
    IN_STOCK,
    Category,
    Color,
    ProductColor,
    ProductItem,
    ProductSize,
    WarehouseItem,
)


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = "__all__"


class ProductColorSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    color = ColorSerializer(read_only=True, many=False)

    class Meta:
        model = ProductColor
        fields = ["image_url", "color"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.image.url)


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    colors = ProductColorSerializer(
        many=True,
        read_only=True,
    )
    size = ProductSizeSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True, many=False)

    quantity = serializers.SerializerMethodField(
        "get_quantity_color_size",
        read_only=True,
    )

    def get_quantity_color_size(self, obj):
        in_stock_items = obj.wh_items.filter(status=IN_STOCK)
        quantities_color_and_sizes = {}

        for item in in_stock_items:
            key = (item.color.title, item.size.value)

            if key not in quantities_color_and_sizes:
                quantities_color_and_sizes[key] = 0
            quantities_color_and_sizes[key] += 1

        return [
            dict(size=size, color=color, quantity=quantity)
            for (color, size), quantity in quantities_color_and_sizes.items()
        ]

    class Meta:
        model = ProductItem
        fields = [
            "id",
            "title",
            "category",
            "description",
            "price",
            "size",
            "colors",
            "quantity",
        ]


class WarehouseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseItem
        fields = "__all__"
