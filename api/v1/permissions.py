from rest_framework import exceptions, permissions


class MethodPermissions(permissions.BasePermission):
    """
    Prohibiting the use of any method other than "delete" for working
    with categories and genres
    """
    def has_permission(self, request, view):
        if view.kwargs:
            if request.method in ['DELETE', 'POST']:
                return True
            raise exceptions.MethodNotAllowed(request.method)
        return True
