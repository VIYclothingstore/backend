from rest_framework import serializers

from delivery.models import Order


class OrderSerializer(serializers.ModelSerializer):
    basket_id = serializers.UUIDField(write_only=True)

    def create(self, validated_data):
        validated_data.pop("basket_id", None)
        return super().create(validated_data)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at", "status", "user")
