from rest_framework.permissions import BasePermission


class IsVerified(BasePermission):

    def has_permission(self, request, view):

        user = request.user
        
        if not user or not user.is_authenticated:
            return False
        
        return user.is_verified