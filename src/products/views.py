from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import IN_STOCK, ProductItem, WarehouseItem
from .serializers import ProductSerializer


class ProductRetrieveAPIView(generics.RetrieveAPIView):
    queryset = ProductItem.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"


class ProductListAPIView(generics.ListAPIView):
    queryset = ProductItem.objects.filter()
    serializer_class = ProductSerializer


class AvailableProductStockAPIView(APIView):

    def get(self, request, *args, **kwargs):
        cont = WarehouseItem.objects.filter(
            product_id=kwargs["product_id"],
            color_id=kwargs["color_id"],
            size_id=kwargs["size_id"],
            status=IN_STOCK,
        ).count()
        return Response({"count": cont})
