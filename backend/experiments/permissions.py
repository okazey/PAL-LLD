from rest_framework.permissions import BasePermission


class IsResearcher(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        role = getattr(user, "role", "")
        return role == "RESEARCHER"


class IsFarmer(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        role = getattr(user, "role", "")
        return role == "FARMER"
