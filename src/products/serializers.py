from rest_framework import serializers

from .models import Picture, Product


class PictureSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Picture
        fields = ["image_url"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.picture.url)


class ProductSerializer(serializers.ModelSerializer):
    images = PictureSerializer(many=True, read_only=True)

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
            "images",
            "color",
            "size",
        ]
