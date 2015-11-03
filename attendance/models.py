from django.db import models

from members.models import BandMember


class EventType(models.Model):
    type = models.CharField(max_length=255, unique=True, verbose_name='Event type')
    points = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Points')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Event(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')
    event_type = models.ForeignKey(EventType, related_name='+', verbose_name='Event type')
    time = models.DateTimeField(verbose_name='Date and time of event')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Attendance(models.Model):
    event = models.ForeignKey(Event, related_name='attendances', verbose_name='Event')
    member = models.ForeignKey(BandMember, related_name='attendances', verbose_name='Band member')
    points = models.DecimalField(max_digits=5, decimal_places=2, null=True, verbose_name='Points')
    check_in_time = models.DateTimeField(null=True, verbose_name='Check-in time')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
