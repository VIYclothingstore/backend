from rest_framework import serializers

from order.models import Basket, BasketItem


class BasketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = "__all__"
        read_only_fields = ["basket"]


class BasketSerializer(serializers.ModelSerializer):
    items = BasketItemSerializer(read_only=True, many=True)

    class Meta:
        model = Basket
        fields = "__all__"
