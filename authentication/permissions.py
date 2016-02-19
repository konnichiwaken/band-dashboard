from rest_framework import permissions

from authentication.utils import is_account_creation_admin


class IsAccountOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, account):
        if request.method == 'PUT':
            return account == request.user

        return False


class CanCreateAccount(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return is_account_creation_admin(request.user)
        elif request.method == 'PUT':
            return True

        return False
