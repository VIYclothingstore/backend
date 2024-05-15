from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import ProductCategory, Color, Product
from .serializers import ProductCategorySerializer, ColorSerializer, ProductSerializer


class ProductCategoryListView(ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = (AllowAny,)


class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = (AllowAny,)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = Product.objects
        price_from = self.request.query_params.get('price')
        price_to = self.request.query_params.get('price')
        if (gender := self.request.query_params.get('gender')) is not None:
            if gender.lower() == 'women':
                queryset = queryset.filter(is_for_women=True)
            elif gender.lower() == 'men':
                queryset = queryset.filter(is_for_men=True)
            elif gender.lower() == 'unisex':
                queryset = queryset.filter(is_for_women=True, is_for_men=True)
            else:
                return Response({'error': 'Invalid gender parameter'}, status=status.HTTP_400_BAD_REQUEST)
        if price_from is not None:
            queryset = queryset.filter(price__gte=price_from)
        if price_to is not None:
            queryset = queryset.filter(price__lte=price_from)

        if (category_id := self.request.query_params.get('category_id')) is not None:
            queryset = queryset.filter(category__id=category_id)

        return queryset
