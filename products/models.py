from django.db import models


class Product(models.Model):
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="products"
    )
