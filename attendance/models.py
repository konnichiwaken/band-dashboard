from datetime import timedelta

from django.db import models
from django.db.models import Q
from django.utils import timezone

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
    unexcused = models.NullBooleanField(verbose_name='Unexcused absence/late')
    is_absence = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def allows_substitution(self):
        if (self.points is None and
            self.is_active and
            self.assigned and
            self.event.time > (timezone.now() + timedelta(days=1))):
            return not SubstitutionForm.objects.filter(
                Q(event_id=self.event_id) &
                Q(requester_id=self.member_id) &
                (
                    Q(status=SubstitutionForm.PENDING) |
                    Q(status=SubstitutionForm.ACCEPTED)
                )).exists()
        else:
            return False


class SubstitutionForm(models.Model):
    ACCEPTED = 'accept'
    DECLINED = 'decline'
    PENDING = 'pending'
    STATUS_CHOICES = (
        (ACCEPTED, 'Accepted'),
        (DECLINED, 'Declined'),
        (PENDING, 'Pending'),
    )

    event = models.ForeignKey(Event, related_name='substitution_forms', verbose_name='Event')
    requester = models.ForeignKey(
        BandMember,
        related_name='substitutions_requested',
        verbose_name='Requester')
    requestee = models.ForeignKey(
        BandMember,
        related_name='substitutions_received',
        verbose_name='Requestee')
    reason = models.CharField(max_length=255, verbose_name='Substitution reason')
    status = models.CharField(
        max_length=255,
        choices=STATUS_CHOICES,
        default=PENDING,
        verbose_name='Status')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def accept(self):
        requester_attendance = Attendance.objects.get(event=self.event, member=requester)
        requester_attendance.is_active = False
        requester_attendance.assigned = False
        requester_attendance.save()

        try:
            requestee_attendance = Attendance.objects.get(event=self.event, member=requestee)
            requestee_attendance.is_active = True
            requestee_attendance.assigned = True
            requestee_attendance.save()
        except Attendance.DoesNotExist:
            Attendance.objects.create(event=self.event, member=requestee, assigned=True)

        self.status = self.ACCEPTED
        self.save()

    def decline(self):
        self.status = self.DECLINED
        self.save()
