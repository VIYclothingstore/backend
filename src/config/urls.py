from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from users import views
from users.views import UserCreateAPIView, UserRetrieveUpdateDestroyAPIView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),

    path("ping/", views.ping, name="Hello world"),
    # ADMIN
    path("admin/", admin.site.urls),
    # TOKEN
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # USER
    path("user/", UserCreateAPIView.as_view(), name="user-create"),
    path(
        "user/<int:pk>",
        UserRetrieveUpdateDestroyAPIView.as_view(),
        name="user-retrieve-update-destroy",
    ),
]
