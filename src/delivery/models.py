import uuid

from django.db import models

from users.models import User

PENDING = "Pending"
PROCESSING = "Processing"
WAITING_FOR_PAYMENT = "Waiting_for_payment"
SHIPPED = "Shipped"
COMPLETED = "Completed"
CANCELED = "Canceled"


class Order(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    street = models.CharField(max_length=20, null=True, blank=True)
    apartment = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            (PENDING, PENDING),
            (PROCESSING, PROCESSING),
            (SHIPPED, SHIPPED),
            (WAITING_FOR_PAYMENT, WAITING_FOR_PAYMENT),
            (COMPLETED, COMPLETED),
            (CANCELED, CANCELED),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
