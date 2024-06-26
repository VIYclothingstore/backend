from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "first_name", "last_name")
    search_fields = ("username", "email", "first_name", "last_name")
    list_filter = ("email", "first_name", "last_name")

    exclude = ["user_permissions", "groups"]
    readonly_fields = [
        "password",
        "date_joined",
        "last_login",
        "is_superuser",
        "email",
    ]
