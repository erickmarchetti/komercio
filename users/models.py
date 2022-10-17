from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.TextField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_seller = models.BooleanField(default=False)

    REQUIRED_FIELDS: list[str] = [
        "first_name",
        "last_name",
    ]
