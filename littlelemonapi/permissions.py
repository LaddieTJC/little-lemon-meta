from rest_framework.permissions import BasePermission

class ManagerOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='Manager'):
            return True
        return False