from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from products.views import ProductListAPIView, ProductRetriveAPIView
from users.serializers import LogoutView
from users.views import (CustomTokenObtainPairView, CustomTokenRefreshView,
                         UserCreateAPIView, UserInfoView,
                         UserRetrieveUpdateDestroyView)

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
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
    # PRODUCTS
    path("products/", ProductListAPIView.as_view(), name="product_list"),
    path("products/<int:id>/", ProductRetriveAPIView.as_view(), name="product_retrive"),
]
