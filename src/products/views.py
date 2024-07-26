import random

from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
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


class ProductSearchView(APIView):
    def get(self, request):

        gender = request.GET.get("gender")
        category = request.GET.get("category")
        title = request.GET.get("title")
        description = request.GET.get("description")
        size = request.GET.get("size")
        color = request.GET.get("color")

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

        if not (title or category or description or color or size or gender):
            return Response(
                {"message": "No search query provided"}, status=HTTP_400_BAD_REQUEST
            )

        products = ProductItem.objects.filter(
            query
        ).distinct()  # Remove duplicate results
        serializer = ProductSerializer(
            products, many=True, context={"request": request}
        )
        return Response(serializer.data, status=HTTP_200_OK)


class ProductSortingView(APIView):
    def get(self, request):
        sort_by = request.GET.get("sort", "popular")

        if sort_by == "price_asc":
            products = ProductItem.objects.all().order_by("price")
        elif sort_by == "price_desc":
            products = ProductItem.objects.all().order_by("-price")
        elif sort_by == "popular":
            products = list(ProductItem.objects.all())
            random.shuffle(products)
        else:
            products = list(ProductItem.objects.all())
            random.shuffle(products)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    

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

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
