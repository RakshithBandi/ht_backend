from rest_framework import permissions

class IsAdminOrManagerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins and managers to edit objects.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the admin or manager users.
        return request.user and request.user.is_authenticated and (
            request.user.groups.filter(name='Admin').exists() or 
            request.user.groups.filter(name='Manager').exists() or
            request.user.is_superuser
        )
