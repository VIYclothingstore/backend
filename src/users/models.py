from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import EmailField
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


class User(AbstractUser):
    email = models.EmailField(max_length=128, unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=128, blank=False, null=False)
    surname = models.CharField(max_length=128, blank=False, null=False)
    last_name = models.CharField(max_length=128, blank=False, null=False)
    phone_number = PhoneNumberField(blank=False, null=False, unique=True)

    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]


def get_full_name(self):
    """
    Return the first_name plus the last_name, with a space in between.
    """

    return f" {self.first_name} {self.last_name}".strip()


def get_short_name(self):
    """Return the short name for the user."""

    return self.first_name


def __str__(self) -> str | EmailField:
    if self.first_name and self.last_name:
        return self.get_full_name()
    else:
        return self.email
