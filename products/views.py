from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from drf_spectacular.utils import extend_schema

from .models import Product
from .serializers import ProductDetailsSerializer, ProductGeneralSerializer
from .permissions import IsSellerOrReadOnly, IsSellerOwnerOrReadOnly


class setSerializerByMethodMixin:
    serializer_by_method = None

    def get_serializer_class(self):

        assert (
            self.serializer_by_method is not None
        ), f"'{self.__class__.__name__}' should include a `serializer_by_method` attribute."

        return self.serializer_by_method.get(self.request.method, self.serializer_class)


class ProductsView(setSerializerByMethodMixin, generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSellerOrReadOnly]

    serializer_by_method = {"GET": ProductGeneralSerializer}

    serializer_class = ProductDetailsSerializer
    queryset = Product.objects.all()

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class ProductsDetailsView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSellerOwnerOrReadOnly]

    serializer_class = ProductDetailsSerializer
    queryset = Product.objects.all()

    @extend_schema(exclude=True)
    def put(self, **kwargs):
        ...
