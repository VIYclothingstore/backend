from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from products.views import ProductCategoryListView, ProductViewSet
from users import views
from users.views import UserCreateAPIView, UserRetrieveUpdateDestroyAPIView, CustomTokenObtainPairView, \
    CustomTokenRefreshView, UserInfoView

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

    # PRODUCT

    path('product/all', ProductViewSet.as_view({'get': 'list'}), name='product-all'),
    path('product/category/', ProductCategoryListView.as_view(), name='product-category'),
    # path('product/<int:pk>/', ProductCategoryDetailView.as_view(), name='product-category-detail'),

]
