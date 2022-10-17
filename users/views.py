from rest_framework import generics, views
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from . import models
from . import serializers


class UserViews(generics.ListCreateAPIView):
    queryset = models.User.objects
    serializer_class = serializers.AccountSerializer


class LoginView(views.APIView):
    def post(self, request: views.Request):
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)
        if not user:
            return views.Response({"detail": "invalid username or password"})

        token, _ = Token.objects.get_or_create(user=user)

        return views.Response({"token": token.key}, views.status.HTTP_200_OK)


class UserFilterLogin(generics.ListAPIView):
    queryset = models.User.objects
    serializer_class = serializers.AccountSerializer

    def get_queryset(self):
        num = self.kwargs.get("num")
        return self.queryset.order_by("date_joined")[0:num]
