from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.db.models import EmailField
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


class User(AbstractUser):
    email = models.EmailField(max_length=128, unique=True, blank=False, null=False)
    first_name = models.CharField(
        max_length=128,
        blank=False,
        null=False,
        validators=[
            RegexValidator(
                r"^[^\d\W]+$",
                "Name can only contain letters and must be at least 1 characters long ",
            ),
            MinLengthValidator(1, "First name must be at least 1 characters long"),
        ],
    )
    surname = models.CharField(
        max_length=128,
        blank=False,
        null=False,
        validators=[
            RegexValidator(r"^[^\d\W]+$", "Surname can only contain letters"),
            MinLengthValidator(1, "Surname must be at least 1 characters long"),
        ],
    )
    last_name = models.CharField(
        max_length=128,
        blank=False,
        null=False,
        validators=[
            RegexValidator(r"^[^\d\W]+$", "Last name can only contain letters"),
            MinLengthValidator(1, "Last name must be at least 1 characters long"),
        ],
    )
    date_of_birth = models.DateField(blank=False, null=False)
    number = PhoneNumberField(r"\+[0-9]{12}", blank=False, null=False)

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
