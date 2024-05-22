from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from users import views
from users.views import (CustomTokenObtainPairView, CustomTokenRefreshView,
                         UserCreateAPIView, UserInfoView,
                         UserRetrieveUpdateDestroyAPIView)

urlpatterns = [
    # API
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("ping/", views.ping, name="Hello world"),
    # ADMIN
    path("admin/", admin.site.urls),
    # TOKEN
    path("auth/token/", CustomTokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("auth/token/refresh/", CustomTokenRefreshView.as_view(), name="token-refresh"),
    # USER
    path("user/create/", UserCreateAPIView.as_view(), name="user-create"),
    path("user/me", UserInfoView.as_view(), name="user-me"),
    path(
        "user/<int:pk>",
        UserRetrieveUpdateDestroyAPIView.as_view(),
        name="user-retrieve-update-destroy",
    ),
    path(
        "user/password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
]
