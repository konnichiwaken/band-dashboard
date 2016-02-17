from rest_framework import permissions


class IsAttendanceAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user:
            user_roles = set(request.user.roles.values_list('name', flat=True))
            attendance_admin_roles = ['Secretary']
            return bool(user_roles.intersection(attendance_admin_roles))

        return False
