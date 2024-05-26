import re
from tokenize import TokenError

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)

from users.models import User


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
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"), username=email, password=password
        )

        if user:
            data = super().validate(attrs)
            data["user_id"] = user.id
            return data
        else:
            return {"message": "Invalid credentials", "code": 400}


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
        self._validate_password(password)
        self._validate_full_name(
            attrs.get("first_name"), attrs.get("last_name"), attrs.get("surname")
        )

        return attrs

    @staticmethod
    def _validate_password(password):
        pattern = r"^(\S){6,}$"
        if not bool(re.match(pattern, password)):
            raise serializers.ValidationError(
                "The password must consist of any characters and have a length of at least 6"
            )

    @staticmethod
    def _validate_full_name(first_name, last_name, surname):
        pattern = r"^[^\d^Ы^ы^Ё^ё^Э^э\W]+$"
        if not bool(re.match(pattern, first_name)):
            raise serializers.ValidationError(
                "The first name can only contain letters and must be at least 1 character long"
            )
        if not bool(re.match(pattern, last_name)):
            raise serializers.ValidationError(
                "The last name can only contain letters and must be at least 1 character long"
            )
        if not bool(re.match(pattern, surname)):
            raise serializers.ValidationError(
                "The surname can only contain letters and must be at least 1 character long"
            )

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
