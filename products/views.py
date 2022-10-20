from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from .models import Product
from .serializers import ProductDetailsSerializer, ProductGeneralSerializer
from .permissions import IsSellerOrReadOnly, IsSellerOwnerOrReadOnly


class ProductsView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSellerOrReadOnly]

    serializer_by_method = {"GET": ProductGeneralSerializer}

    serializer_class = ProductDetailsSerializer
    queryset = Product.objects.all()

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    def get_serializer_class(self):
        return self.serializer_by_method.get(self.request.method, self.serializer_class)


class ProductsDetailsView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSellerOwnerOrReadOnly]

    serializer_class = ProductDetailsSerializer
    queryset = Product.objects.all()
