from django.contrib import admin
from django.urls import path

from users import views
from users.views import UserCreateAPIView, UserRetrieveUpdateDestroyAPIView, CustomTokenObtainPairView, \
    CustomTokenRefreshView, UserInfoView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),

    path("ping/", views.ping, name="Hello world"),
    # ADMIN
    path("admin/", admin.site.urls),
    # TOKEN
    path("token/", CustomTokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token-refresh"),
    # USER
    path("user/", UserCreateAPIView.as_view(), name="user-create"),
    path("user/me", UserInfoView.as_view(), name="user-me"),
    path(
        "user/<int:pk>",
        UserRetrieveUpdateDestroyAPIView.as_view(),
        name="user-retrieve-update-destroy",
    ),
]
