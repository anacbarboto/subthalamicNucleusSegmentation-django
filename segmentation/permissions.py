from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and
            request.user.profile and
            request.user.profile.is_admin
        )


class IsSpecialist(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and
            request.user.profile and
            request.user.profile.is_specialist
        )