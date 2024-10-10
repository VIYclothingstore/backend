import uuid

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from users.models import User

PENDING = "Pending"
PROCESSING = "Processing"
WAITING_FOR_PAYMENT = "Waiting_for_payment"
SHIPPED = "Shipped"
COMPLETED = "Completed"
CANCELED = "Canceled"
PAYMENT_OK = "Payment_Ok"

BRANCH = "Branch"
COURIER = "Courier"
PARCEL_LOCKER = "Parcel Locker"

CARD = "Card"
UPON_RECEIPT = "Upon Receipt"


class Order(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    surname = models.CharField(max_length=100, null=False, blank=False)
    phone_number = PhoneNumberField(blank=False, null=False)
    email = models.EmailField(max_length=100, null=False, blank=False)
    city = models.CharField(max_length=100, null=False, blank=False)
    delivery_method = models.CharField(
        max_length=48,
        choices=[
            (BRANCH, BRANCH),
            (COURIER, COURIER),
            (PARCEL_LOCKER, PARCEL_LOCKER),
        ],
        null=False,
        blank=False,
    )
    branch = models.CharField(max_length=100, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    apartment = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            (PENDING, PENDING),
            (PROCESSING, PROCESSING),
            (SHIPPED, SHIPPED),
            (WAITING_FOR_PAYMENT, WAITING_FOR_PAYMENT),
            (PAYMENT_OK, PAYMENT_OK),
            (COMPLETED, COMPLETED),
            (CANCELED, CANCELED),
        ],
    )
    payment_method = models.CharField(
        max_length=48,
        choices=[
            (CARD, CARD),
            (UPON_RECEIPT, UPON_RECEIPT),
        ],
        null=False,
        blank=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
