from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from delivery.serializers import (
    NovaPostAddressesView,
    NovaPostSettlementsView,
    NovaPostWarehousesView,
)
from products.views import (
    AvailableProductStockAPIView,
    ProductListAPIView,
    ProductRetrieveAPIView,
    ProductSearchView,
    ProductSortingView,
)
from users.serializers import LogoutView
from users.views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    UserCreateAPIView,
    UserInfoView,
    UserRetrieveUpdateDestroyView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Sport Hub | SportHub API",
        default_version="v1",
        contact=openapi.Contact(email="vitasyushchyk@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # ADMIN
    path("admin/", admin.site.urls),
    # TOKEN
    path(
        "auth/token/refresh/",
        CustomTokenRefreshView.as_view(),
        name="token-refresh",
    ),
    # USER
    path("user/registration/", UserCreateAPIView.as_view(), name="user-registration"),
    path("user/login/", CustomTokenObtainPairView.as_view(), name="user-login"),
    path("user/logout/", LogoutView.as_view(), name="logout"),
    path("user/me/", UserInfoView.as_view(), name="user-me"),
    path(
        "user/profile/",
        UserRetrieveUpdateDestroyView.as_view(),
        name="user-retrieve-update-destroy",
    ),
    path(
        "user/password_reset/",
        include("django_rest_passwordreset.urls", namespace="password-reset"),
    ),
    # PRODUCTS
    path("products/", ProductListAPIView.as_view(), name="product-list"),
    path(
        "products/<int:id>/", ProductRetrieveAPIView.as_view(), name="product-retrieve"
    ),
    path(
        "products/<int:product_id>/<int:color_id>/<int:size_id>/available/",
        AvailableProductStockAPIView.as_view(),
        name="product-available-stock",
    ),
    path("products/search/", ProductSearchView.as_view(), name="product-search"),
    path("products/sort/", ProductSortingView.as_view(), name="product-sorting"),
    # NOVA POST
    path(
        "nova-post/settlements/<str:settlement_name>/",
        NovaPostSettlementsView.as_view(),
        name="nova-post-settlements",
    ),
    path(
        "nova-post/warehouses/<str:settlement_name>/<str:warehouse_id>/",
        NovaPostWarehousesView.as_view(),
        name="nova-get-warehouses",
    ),
    path(
        "nova-post/search_streets/<str:street_name>/<str:ref>/",
        NovaPostAddressesView.as_view(),
        name="nova-search-street",
    ),
]
