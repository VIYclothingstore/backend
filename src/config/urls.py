from django.contrib import admin
from django.urls import path

from users.views import UserCreateAPIView, UserRetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
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
