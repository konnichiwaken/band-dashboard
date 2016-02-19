from rest_framework import permissions

from attendance.utils import is_attendance_admin


class IsAttendanceAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user
        if user:
            return is_attendance_admin(user)

        return False


class IsAttendanceAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user:
            return is_attendance_admin(user)

        return False
