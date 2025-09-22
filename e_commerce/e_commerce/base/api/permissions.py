from rest_framework.permissions import BasePermission
from base.models import User
    

class UnAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated