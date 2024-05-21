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
            "date_of_birth",
            "number",
        )

    def validate(self, attrs):
        password = attrs.get("password")
        repeat_password = attrs.get("repeat_password")
        if password != repeat_password:
            raise serializers.ValidationError("Passwords do not match.")
        attrs.pop("repeat_password", None)
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["email"],
            validated_data["password"],
            username=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            surname=validated_data["surname"],
            date_of_birth=validated_data["date_of_birth"],
            number=validated_data["number"],
        )
        user.save()
        return user


class UserRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            f"first_name",
            "last_name",
            "surname",
            "date_of_birth",
            "number",
        )


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
