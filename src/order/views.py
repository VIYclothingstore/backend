from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from order.models import BasketItem
from order.serializers import BasketItemSerializer, BasketSerializer
from products.models import IN_STOCK, WarehouseItem


class CreateBasket(generics.CreateAPIView):
    serializer_class = BasketSerializer


class RetrieveUpdateDestroyBasketAPIView(viewsets.ModelViewSet):
    serializer_class = BasketItemSerializer
    queryset = BasketItem.objects.all()
    lookup_field = "basket_id"

    def _check_warehouse_availability(self, product_id, color_id, size_id, quantity):
        available_stock = WarehouseItem.objects.filter(
            product_id=product_id,
            color_id=color_id,
            size_id=size_id,
            status=IN_STOCK,
        ).count()

        if available_stock < quantity:
            return Response(
                {"detail": "Sorry, but this product is out of stock"},
                status=HTTP_400_BAD_REQUEST,
            )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data.get("product")
        color_id = serializer.validated_data.get("color")
        size_id = serializer.validated_data.get("size")
        quantity = serializer.validated_data.get("quantity")
        warehouse_check_response = self._check_warehouse_availability(
            product_id, color_id, size_id, quantity
        )
        if warehouse_check_response:
            return warehouse_check_response
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data.get("product")
        color_id = serializer.validated_data.get("color")
        size_id = serializer.validated_data.get("size")
        quantity = serializer.validated_data.get("quantity")
        warehouse_check_response = self._check_warehouse_availability(
            product_id, color_id, size_id, quantity
        )
        if warehouse_check_response:
            return warehouse_check_response
        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)
