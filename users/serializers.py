from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

from drf_spectacular.utils import extend_schema_serializer
from drf_spectacular.utils import OpenApiExample


class AccountSerializer(serializers.ModelSerializer):
    is_seller = serializers.BooleanField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_superuser",
            "is_active",
        ]
        read_only_fields = [
            "id",
            "date_joined",
            "is_superuser",
            "is_active",
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class AccountUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "password",
            "username",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_superuser",
            "is_active",
        ]
        read_only_fields = [
            "id",
            "is_seller",
            "date_joined",
            "is_superuser",
            "is_active",
        ]

    def update(self, instance, validated_data):
        new_password = validated_data.get("password")

        if not new_password is None:
            validated_data["password"] = make_password(new_password)

        return super().update(instance, validated_data)


class AccountUpdateActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_superuser",
            "is_active",
        ]
        read_only_fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_superuser",
        ]


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Rota de login",
            value={"token": "string"},
            request_only=False,
            response_only=True,
        )
    ],
)
class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
        ]
