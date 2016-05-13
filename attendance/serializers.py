import datetime

from rest_framework import serializers

from attendance.models import Attendance
from attendance.models import Event
from attendance.models import EventType
from attendance.utils import calculate_attendance_points
from authentication.models import Account
from members.models import Band
from members.serializers import BandMemberSerializer
from members.serializers import BandSerializer


class EventTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventType
        fields = (
            'id',
            'name',
            'points',
            'ready_to_play',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('created_at', 'updated_at',)


class EventSerializer(serializers.ModelSerializer):
    type = EventTypeSerializer(required=False)
    type_id = serializers.IntegerField(min_value=0)
    band = BandSerializer(required=False)
    band_id = serializers.IntegerField(min_value=0, required=False)

    class Meta:
        model = Event
        fields = (
            'id',
            'title',
            'time',
            'type',
            'type_id',
            'band',
            'band_id',
            'points',
            'ready_to_play',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('created_at', 'updated_at',)

    def create(self, validated_data):
        band_id = validated_data.pop('band_id', 0)
        if band_id:
            band = Band.objects.get(id=band_id)
            validated_data['band'] = band

        event_type_id = validated_data.pop('type_id')
        validated_data['type'] = EventType.objects.get(id=event_type_id)
        event = Event.objects.create(**validated_data)
        if band_id:
            for member in band.assigned_members.all():
                Attendance.objects.create(event=event, member=member, assigned=True)

        return event


class AttendanceSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    event_id = serializers.IntegerField(min_value=0)
    member = BandMemberSerializer(read_only=True)
    member_id = serializers.IntegerField(min_value=0)
    is_late = serializers.BooleanField(required=False)

    class Meta:
        model = Attendance
        fields = (
            'id',
            'event',
            'event_id',
            'member',
            'member_id',
            'points',
            'check_in_time',
            'assigned',
            'unexcused',
            'is_absence',
            'created_at',
            'updated_at',
            'is_late',
        )
        read_only_fields = ('created_at', 'updated_at',)

    def create(self, validated_data):
        check_in_time = validated_data.get('check_in_time', None)
        is_late = validated_data.pop('is_late', None)
        event_id = validated_data.get('event_id', None)
        assigned = validated_data.get('assigned', None)
        if event_id:
            event = Event.objects.get(id=event_id)

        if is_late:
            if check_in_time:
                event_time = event.time
                new_check_in_time = event_time.replace(
                    hour=check_in_time.hour,
                    minute=check_in_time.minute)
                if new_check_in_time < event_time:
                    new_check_in_time = new_check_in_time + datetime.timedelta(days=1)

                validated_data['points'] = calculate_attendance_points(
                    event,
                    assigned,
                    check_in_time=new_check_in_time,
                    unexcused=validated_data.get('unexcused', False))
                validated_data['check_in_time'] = new_check_in_time
        else:
            validated_data['points'] = calculate_attendance_points(event, assigned)
            validated_data['check_in_time'] = None

        attendance = Attendance.objects.create(**validated_data)
        return attendance

    def update(self, instance, validated_data):
        check_in_time = validated_data.get('check_in_time', None)
        is_late = validated_data.pop('is_late', None)
        event = instance.event
        assigned = validated_data.get('assigned', None)
        if validated_data.get('is_absence', None):
            validated_data['check_in_time'] = None
            validated_data['points'] = 0
        else:
            if is_late:
                if check_in_time:
                    event_time = event.time
                    new_check_in_time = event_time.replace(
                        hour=check_in_time.hour,
                        minute=check_in_time.minute)
                    if new_check_in_time < event_time:
                        new_check_in_time = new_check_in_time + datetime.timedelta(days=1)

                    points = calculate_attendance_points(
                        new_check_in_time,
                        event,
                        validated_data.get('unexcused', None),
                        assigned)
                    validated_data['check_in_time'] = new_check_in_time
                    validated_data['points'] = points
            else:
                validated_data['check_in_time'] = None
                points = event.points if assigned else event.points / 2
                validated_data['points'] = points

        attendance = Attendance.objects.get(id=instance.id)
        for field, value in validated_data.iteritems():
            setattr(attendance, field, value)

        return attendance
