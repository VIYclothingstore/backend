import uuid
from datetime import timedelta

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from config import settings


class CustomUserManager(BaseUserManager):
    @staticmethod
    def send_confirmation_email(user):
        email_confirmation = ConfirmationUserEmail.objects.create(user=user)
        email_text_message = (
            f"{user.first_name},\n\n"
            "Ми раді вітати тебе в спільноті Online store Sport Hub!\n"
            "Щоб завершити реєстрацію та отримати доступ до всіх можливостей нашого магазину, будь ласка, "
            "підтвердь свою електронну адресу, перейшовши за посиланням:\n\n"
            f"{settings.UI_URLS['confirmed_email']}"
            f"/{email_confirmation.token}\n\n"
            "Якщо у тебе виникнуть будь-які питання, звертайся до нас за адресою sporthub.store.ua@gmail.com\n\n"
            "З найкращими побажаннями,\n"
            "Команда Online store Sport Hub"
        )

        msg = EmailMultiAlternatives(
            "Підтвердження реєстрації на Online store Sport Hub",
            email_text_message,
            "shop_onlinee@ukr.net",
            [user.email],
        )
        msg.send()

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The email must be set")

        extra_fields.setdefault("is_active", False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(user)
        self.send_confirmation_email(user)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("username", email)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


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
        """
        Return the short name for the user.
        """
        return self.first_name

    def __str__(self) -> str:
        if self.first_name and self.last_name:
            return self.get_full_name()
        else:
            return str(self.email)


class ConfirmationUserEmail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_token_valid(self):
        token_lifetime = timedelta(seconds=settings.TOKEN_FOR_EMAIL_LIFETIME)
        expiration_date = self.created_at + token_lifetime
        return expiration_date >= timezone.now()
