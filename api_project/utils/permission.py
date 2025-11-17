from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    message = 'You must be an admin to perform this action.'

    def has_permission(self, request, view):
        if request.method in ['GET','PUT','DELETE']:
            return True
        return request.user.is_staff


class IsVerified(BasePermission):
    message = 'You must be verified to perform this action.'

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        verify = hasattr(user, 'profile')
        return verify and user.profile.verified

