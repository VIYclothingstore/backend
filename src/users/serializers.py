import re
from tokenize import TokenError

from django.contrib.auth import logout
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)

from users.models import User
from users.validators import CustomFullNameValidator, CustomPasswordValidator


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer for tokens obtaining process.
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        """
        Validate the provided credentials and returns created token (access token and refresh token)
        with added user_id field.
        """
        data = super().validate(attrs)
        data["user_id"] = self.user.id
        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """
    Custom TokenRefreshSerializer to handle token refresh.
    """

    refresh = serializers.CharField(allow_blank=True)

    def validate(self, attrs):
        """
        Validate the token and return the data if it's valid.
        """
        if not attrs.get("refresh"):
            return {"message": "Field 'refresh' may not be blank.", "code": 400}

        try:
            data = super().validate(attrs)
            return data
        except TokenError as e:
            return {"message": str(e), "code": 500}


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    repeat_password = serializers.CharField(write_only=True)

    class Meta:
        model = User

        fields = (
            "email",
            "password",
            "repeat_password",
            "first_name",
            "last_name",
            "surname",
            "phone_number",
        )

    def validate(self, attrs):
        password = attrs.get("password")
        repeat_password = attrs.pop("repeat_password", None)
        if password != repeat_password:
            raise serializers.ValidationError("Passwords do not match.")
        password_validator = CustomPasswordValidator()
        password_validator.validate(password)
        full_name_validator = CustomFullNameValidator()
        full_name_validator.validate(
            attrs.get("first_name"), attrs.get("last_name"), attrs.get("surname")
        )

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["email"],
            validated_data["password"],
            username=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            surname=validated_data["surname"],
            phone_number=validated_data["phone_number"],
        )
        user.save()
        return user


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)

        return Response(
            {"message": "Successfully logged out!"}, status=status.HTTP_200_OK
        )


class UserRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "surname",
            "phone_number",
        )
