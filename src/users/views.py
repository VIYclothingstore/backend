from tokenize import TokenError

from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from requests import Request
from rest_framework import exceptions as rf_exceptions
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.models import User
from users.permission import IsOwner
from users.serializers import (
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer,
    UserCreateSerializer,
    UserRetrieveUpdateDestroySerializer,
)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except rf_exceptions.ValidationError as e:
            msg = "\n".join(
                [f"Field '{key}' may not be blank." for key in e.detail.keys()]
            )
            return Response(
                data={"message": msg, "code": 400}, status=status.HTTP_400_BAD_REQUEST
            )
        except TokenError as e:
            return Response(
                data={"message": ", ".join(e.args), "code": 500},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        try:
            _ = serializer.validated_data["code"]
            return Response(
                serializer.validated_data, status=status.HTTP_400_BAD_REQUEST
            )
        except KeyError:
            return Response(serializer.validated_data, status=status.HTTP_200_OK)


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        try:
            if serializer.validated_data["access"]:
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
        except KeyError:
            if serializer.validated_data["code"] == status.HTTP_400_BAD_REQUEST:
                status_code = status.HTTP_400_BAD_REQUEST
            else:
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            return Response(data=serializer.validated_data, status=status_code)


class UserInfoView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserRetrieveUpdateDestroySerializer

    def get_object(self):
        return self.request.user


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)


class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwner]
    serializer_class = UserRetrieveUpdateDestroySerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        partial = False
        return self.update(request, *args, **kwargs, partial=partial)

    def patch(self, request, *args, **kwargs):
        partial = True
        return self.update(request, *args, **kwargs, partial=partial)


@receiver(reset_password_token_created)
def password_reset_token_created(instance, reset_password_token, *args, **kwargs):
    email_text_message = (
        f"{reset_password_token.user.first_name},\n\n"
        "Запит на скидання пароля для dfijuj облікового запису.\n"
        f"Перейдіть за посиланням, щоб скинути пароль:\n\n"
        # f"{settings.UI}/{settings.UI_URLS['confirm_reset_password']}"
        f"{instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm'))}"
        f"?token={reset_password_token.key}\n\n"
        "Якщо ви не запитували скидання пароля, проігноруйте цей лист.\n\n"
        "Дякуємо,\n"
        "З повагою команда  Online store Sport Hub"
    )

    msg = EmailMultiAlternatives(
        # Subject:
        "Скидання пароля для Online store Sport Hub.",
        # Message:
        email_text_message,
        # From:
        "shop_onlinee@ukr.net",
        # To:
        [reset_password_token.user.email],
    )
    msg.send()
