from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from . import serializers, models
from .permissions import IsSellerOrReadOnly


class ProductsView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSellerOrReadOnly]

    serializer_by_method = {"GET": serializers.ProductGeneralSerializer}

    serializer_class = serializers.ProductDetailsSerializer
    queryset = models.Product.objects

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    def get_serializer_class(self):
        return self.serializer_by_method.get(self.request.method, self.serializer_class)
