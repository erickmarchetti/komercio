from rest_framework.permissions import BasePermission


class IsSellerOrReadOnly(BasePermission):
    def has_permission(self, request, view):

        return (
            request.method == "GET"
            or request.user.is_authenticated
            and request.user.is_seller
        )
