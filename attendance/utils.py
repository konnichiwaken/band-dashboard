import copy
import datetime
import math

from decimal import Decimal


def calculate_attendance_points(check_in_time, event):
    time_delta = check_in_time - event.time
    minutes_late = divmod(time_delta.days * 86400 + time_delta.seconds, 60)[0]
    point_intervals = Decimal(math.ceil(Decimal(minutes_late) / 15))
    points_deducted = point_intervals * Decimal(0.5)
    attendance_points = event.points - points_deducted - 1
    if attendance_points < 0:
        attendance_points = 0

    return attendance_points
