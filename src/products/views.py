from django.core.exceptions import ObjectDoesNotExist
from requests import Response
from rest_framework import generics, views

from .models import ProductItem, WarehouseItem
from .serializers import ProductSerializer


class ProductRetrieveAPIView(generics.RetrieveAPIView):
    queryset = ProductItem.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"


class ProductListAPIView(generics.ListAPIView):
    queryset = ProductItem.objects.filter()
    serializer_class = ProductSerializer


# ToDo (Vita): зробити нову апішку, де за id продукта можна було дивитись скільки продуктів певного кольору та розміру,
#  бо нині рахується загальна кількість (наприклад білі кросовки пума 38 р - 5 штук, білі кросовки пума 39 - 4 штуки, чорні кросовки пума 40 р - 4ш)


# class AvailableProductAPIView(views.APIView):
#
#     def get(self, request, product_id, *args, **kwargs):
#
