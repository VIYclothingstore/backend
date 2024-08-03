from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet

from order.models import Basket, BasketItem
from order.serializers import BasketItemSerializer, BasketSerializer
from products.models import IN_STOCK, WarehouseItem


class CreateBasket(mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = BasketSerializer
    lookup_url_kwarg = "basket_id"
    queryset = Basket.objects.all()


class RetrieveUpdateDestroyBasketAPIView(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = BasketItemSerializer
    queryset = BasketItem.objects.all()
    lookup_url_kwarg = "basket_item_id"

    def _check_warehouse_availability(self, serializer):
        product_id = serializer.validated_data.get("product")
        color_id = serializer.validated_data.get("color")
        size_id = serializer.validated_data.get("size")
        quantity = serializer.validated_data.get("quantity")
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
        warehouse_check_response = self._check_warehouse_availability(serializer)
        if warehouse_check_response:
            return warehouse_check_response
        serializer.save(**kwargs)
        return Response(serializer.data, status=HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        warehouse_check_response = self._check_warehouse_availability(serializer)
        if warehouse_check_response:
            return warehouse_check_response
        serializer.save(**kwargs)
        return Response(serializer.data, status=HTTP_200_OK)
