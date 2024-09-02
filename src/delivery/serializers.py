from rest_framework import serializers

from delivery.models import Order


class OrderSerializer(serializers.ModelSerializer):
    basket_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at", "status")
