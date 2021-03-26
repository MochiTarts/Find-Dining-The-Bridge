from rest_framework import permissions
from utils.common import get_user

class ROPermission(permissions.BasePermission):
    """
    permission check for RO.
    """

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.role == 'RO')
