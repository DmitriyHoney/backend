from rest_framework import permissions


class OnlyAdminOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user and (request.user.is_moderator() or request.user.is_admin()))
