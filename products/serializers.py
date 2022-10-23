from rest_framework import serializers

from users.serializers import AccountSerializer

from .models import Product


class ProductDetailsSerializer(serializers.ModelSerializer):
    seller = AccountSerializer(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["id"]


class ProductGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "description",
            "price",
            "quantity",
            "is_active",
            "seller_id",
        ]
        read_only_fields = [
            "id",
            "description",
            "price",
            "quantity",
            "is_active",
            "seller_id",
        ]
