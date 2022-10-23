from django.urls import path
from . import views

urlpatterns = [
    path(
        "products/", views.ProductListCreateView.as_view(), name="product_list_create"
    ),
    path("products/<str:pk>/", views.ProductRetrieveUpdateView.as_view()),
]
