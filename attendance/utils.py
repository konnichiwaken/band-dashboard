import copy
import datetime
import math

from decimal import Decimal

from attendance.settings import ATTENDANCE_ADMIN_ROLES


def calculate_attendance_points(event, assigned, check_in_time=None, unexcused=False):
    if check_in_time:
        time_delta = check_in_time - event.time
        minutes_late = divmod(time_delta.days * 86400 + time_delta.seconds, 60)[0]
    else:
        minutes_late = 0

    point_intervals = Decimal(math.ceil(Decimal(minutes_late) / 15))
    if unexcused:
        points_deducted = point_intervals * Decimal(0.5) + 1
    else:
        points_deducted = point_intervals * Decimal(0.25)

    base_points = event.points
    if not assigned and event.band:
        base_points /= 2

    attendance_points = base_points - points_deducted
    if attendance_points < 0:
        attendance_points = 0

    return attendance_points


def is_attendance_admin(account):
    roles = set(account.roles.values_list('name', flat=True))
    return bool(roles.intersection(ATTENDANCE_ADMIN_ROLES))
