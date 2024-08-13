from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
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


class ProductSearchView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        gender = self.request.GET.get("gender")
        category = self.request.GET.get("category")
        title = self.request.GET.get("title")
        description = self.request.GET.get("description")
        size = self.request.GET.get("size")
        color = self.request.GET.get("color")

        query = Q()
        if gender:
            query &= Q(category__gender__iexact=gender)
        if category:
            query &= Q(category__sub_category__icontains=category)

        if title:
            query &= Q(title__icontains=title)

        if description:
            query &= Q(description__icontains=description)
        if size:
            query &= Q(size__value=size)
        if color:
            query &= Q(colors__color__title__iexact=color)
        products = ProductItem.objects.filter(query).distinct()
        return products


class ProductSortingView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        sort_by = self.request.GET.get("sort")
        queryset = ProductItem.objects.all()

        if sort_by == "price_asc":
            queryset = queryset.order_by("price")
        elif sort_by == "price_desc":
            queryset = queryset.order_by("-price")
        elif sort_by == "popular":
            queryset = queryset.order_by("?")
        elif sort_by == "created_at":
            queryset = queryset.order_by("-created_at")
        elif sort_by == "updated_at":
            queryset = queryset.order_by("-updated_at")
        elif sort_by == "is_latest":
            queryset = queryset.order_by("category", "-created_at").distinct("category")

        return queryset


class ProductFilterView(APIView):
    def get(self, request):
        sizes = request.query_params.getlist("sizes")
        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")
        colors = request.query_params.getlist("colors")
        gender = request.query_params.get("gender")

        filters = Q()

        if gender:
            filters &= Q(category__gender=gender)
        if sizes:
            filters &= Q(size__value__in=sizes)
        if min_price and max_price:
            filters &= Q(price__gte=min_price, price__lte=max_price)
        if colors:
            filters &= Q(color__title__in=colors)

        products = ProductItem.objects.filter(filters).distinct()

        serializer = ProductSerializer(
            products, many=True, context={"request": request}
        )
        return Response(serializer.data, status=HTTP_200_OK)
