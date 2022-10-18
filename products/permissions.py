from rest_framework.permissions import BasePermission


class IsSellerOrReadOnly(BasePermission):
    def has_permission(self, request, view):

        return (
            request.method == "GET"
            or request.user.is_authenticated
            and request.user.is_seller
        )


class IsSellerOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):

        return (
            request.method == "GET"
            or request.user.is_authenticated
            and request.user == obj.seller
        )
