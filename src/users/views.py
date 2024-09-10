from tokenize import TokenError

from django.contrib.auth import logout
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from requests import Request
from rest_framework import exceptions as rf_exceptions
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_406_NOT_ACCEPTABLE,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from config import settings
from users.models import ConfirmationUserEmail, CustomUserManager, User
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
        if (
            user := User.objects.filter(email=serializer.initial_data["email"]).first()
        ) and not user.is_active:
            return Response(
                data=dict(
                    msg="User not activated, please activate your account by email"
                ),
                status=HTTP_406_NOT_ACCEPTABLE,
            )
        try:
            serializer.is_valid(raise_exception=True)
        except rf_exceptions.ValidationError as e:
            msg = "\n".join(
                [f"Field '{key}' may not be blank." for key in e.detail.keys()]
            )
            return Response(data=dict(msg=msg), status=HTTP_400_BAD_REQUEST)
        except TokenError as e:
            return Response(
                data=dict(
                    msg=", ".join(e.args),
                    status=HTTP_500_INTERNAL_SERVER_ERROR,
                )
            )
        try:
            _ = serializer.validated_data["code"]
            return Response(serializer.validated_data, status=HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response(serializer.validated_data, status=HTTP_200_OK)


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        try:
            if serializer.validated_data["access"]:
                return Response(serializer.validated_data, status=HTTP_200_OK)
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


class UserActivationView(APIView):
    def post(self, _: Request, activation_key):
        try:
            user = User.objects.get(confirmationuseremail__token=activation_key)
            confirmation_email = user.confirmationuseremail_set.get(
                token=activation_key
            )
            if not confirmation_email.is_token_valid():
                return Response(
                    data=dict(
                        msg="The activation key to confirm the user's expired. Please request a new one."
                    ),
                    status=HTTP_400_BAD_REQUEST,
                )
            user.is_active = True
            user.save()
            user.confirmationuseremail_set.all().delete()
            return Response(
                data=dict(msg="Congratulations, user activated successfully."),
                status=HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                data=dict(msg="Invalid activation key"),
                status=HTTP_400_BAD_REQUEST,
            )


class ResendActivationEmailView(APIView):
    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response(
                data=dict(msg="Email is required"),
                status=HTTP_400_BAD_REQUEST,
            )
        try:
            inactive_user = User.objects.get(email=email)
            existing_token = ConfirmationUserEmail.objects.filter(
                user=inactive_user
            ).first()
            if existing_token and existing_token.is_token_valid():
                return Response(
                    data=dict(
                        msg="Activation email already sent. Please check your inbox."
                    ),
                    status=HTTP_200_OK,
                )
            CustomUserManager.send_confirmation_email(inactive_user)
            return Response(
                data=dict(msg="Activation email sent"),
                status=HTTP_200_OK,
            )
        except ConfirmationUserEmail.DoesNotExist:
            return Response(
                data=dict(msg="User nor found"),
                status=HTTP_404_NOT_FOUND,
            )


class UserRetrieveUpdateDestroyView(UpdateAPIView, DestroyAPIView):
    permission_classes = [IsOwner]
    serializer_class = UserRetrieveUpdateDestroySerializer
    queryset = User.objects.all()

    def get_object(self):
        user = super().get_object()
        if user.id != self.request.user.id:
            raise PermissionDenied("You cannot access another user's profile.")
        return user

    def put(self, request, *args, **kwargs):
        partial = False
        return self.update(request, *args, **kwargs, partial=partial)

    def patch(self, request, *args, **kwargs):
        partial = True
        return self.update(request, *args, **kwargs, partial=partial)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(
            data=dict(msg="Successfully logged out!"),
            status=HTTP_200_OK,
        )


@receiver(reset_password_token_created)
def password_reset_token_created(reset_password_token, *args, **kwargs):
    email_text_message = (
        f"{reset_password_token.user.first_name},\n\n"
        "Запит на скидання пароля для вашого облікового запису.\n"
        "Перейдіть за посиланням, щоб скинути пароль:\n\n"
        f"{settings.UI_URLS['confirm_reset_password']}"
        f"/{reset_password_token.key}\n\n"
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
