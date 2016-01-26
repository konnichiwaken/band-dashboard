from django.db import models

from members.models import Band
from members.models import BandMember


class EventType(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Event type name')
    points = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Points')
    ready_to_play = models.IntegerField(verbose_name='Minutes before event for RTP')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Event(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')
    time = models.DateTimeField(verbose_name='Date and time of event')
    type = models.ForeignKey(EventType, related_name='events', verbose_name='Event type')
    band = models.ForeignKey(Band, related_name='events', null=True, verbose_name='Band')
    points = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Points')
    ready_to_play = models.IntegerField(verbose_name='Minutes before event for RTP')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Attendance(models.Model):
    event = models.ForeignKey(Event, related_name='attendances', verbose_name='Event')
    member = models.ForeignKey(BandMember, related_name='attendances', verbose_name='Band member')
    points = models.DecimalField(max_digits=5, decimal_places=2, null=True, verbose_name='Points')
    check_in_time = models.DateTimeField(null=True, verbose_name='Check-in time')
    is_active = models.BooleanField(default=True, verbose_name='Is active')
    assigned = models.BooleanField(verbose_name='Assigned to event')
    unexcused = models.BooleanField(default=False, verbose_name='Unexcused absence')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
