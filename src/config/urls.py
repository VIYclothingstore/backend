from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

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
)
from users.serializers import LogoutView
from users.views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    UserCreateAPIView,
    UserInfoView,
    UserRetrieveUpdateDestroyView,
)

urlpatterns = [
    # API
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    # ADMIN
    path("admin/", admin.site.urls),
    # TOKEN
    path("auth/token/refresh/", CustomTokenRefreshView.as_view(), name="token-refresh"),
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
