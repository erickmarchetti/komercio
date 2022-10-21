from rest_framework import generics, views
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import authenticate

from drf_spectacular.utils import extend_schema

from . import models, serializers
from .permissions import IsOwnerOfAccount


class UserListCreateView(generics.ListCreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.AccountSerializer


class LoginView(views.APIView):
    # apenas para complementar a documentação
    serializer_class = serializers.LoginSerializer

    def post(self, request: views.Request):
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)
        print(user, type(user))
        if not user:
            return views.Response(
                {"detail": "invalid username or password"},
                views.status.HTTP_400_BAD_REQUEST,
            )

        token, _ = Token.objects.get_or_create(user=user)

        return views.Response({"token": token.key}, views.status.HTTP_200_OK)


class UserListByNumView(generics.ListAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.AccountSerializer

    def get_queryset(self):
        num = self.kwargs.get("num")
        return self.queryset.order_by("date_joined")[0:num]


class UserUpdateView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOfAccount]

    queryset = models.User.objects.all()
    serializer_class = serializers.AccountUpdateSerializer

    @extend_schema(exclude=True)
    def put(self, **kwargs):
        ...


class UserUpdateActivityView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = models.User.objects.all()
    serializer_class = serializers.AccountUpdateActivitySerializer

    @extend_schema(exclude=True)
    def put(self, **kwargs):
        ...
