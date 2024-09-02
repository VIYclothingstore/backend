from django.contrib import admin

from delivery.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "first_name",
        "last_name",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = ("id", "user__username", "first_name", "last_name", "status")
    list_filter = ("status", "created_at", "updated_at")
