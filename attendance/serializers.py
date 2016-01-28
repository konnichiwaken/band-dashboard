import datetime

from rest_framework import serializers

from attendance.models import Attendance
from attendance.models import Event
from attendance.models import EventType
from attendance.utils import calculate_attendance_points
from members.models import Band
from members.serializers import BandMemberSerializer
from members.serializers import BandSerializer


class EventTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventType
        fields = ('id',
            'name',
            'points',
            'ready_to_play',
            'created_at',
            'updated_at',)
        read_only_fields = ('created_at', 'updated_at',)


class EventSerializer(serializers.ModelSerializer):
    type = EventTypeSerializer(required=False)
    band = BandSerializer(required=False)
    type_id = serializers.IntegerField(min_value=0)
    band_id = serializers.IntegerField(min_value=0)

    class Meta:
        model = Event
        fields = ('id',
            'title',
            'created_at',
            'updated_at',
            'time',
            'type',
            'band',
            'type_id',
            'band_id',
            'points',
            'ready_to_play',)
        read_only_fields = ('created_at', 'updated_at',)

    def create(self, validated_data):
        type_id = validated_data.pop('type_id')
        band_id = validated_data.pop('band_id')
        type = EventType.objects.get(id=type_id)
        band = Band.objects.get(id=band_id)
        event = Event.objects.create(band=band, type=type, **validated_data)
        for member in band.assigned_members.all():
            Attendance.objects.create(event=event, member=member, assigned=True)

        return event


class AttendanceSerializer(serializers.ModelSerializer):
    member = BandMemberSerializer(read_only=True)
    member_id = serializers.IntegerField(min_value=0)
    is_late = serializers.BooleanField(required=False)
    event_id = serializers.IntegerField(min_value=0)

    class Meta:
        model = Attendance
        fields = (
            'id',
            'member',
            'member_id',
            'check_in_time',
            'points',
            'event_id',
            'is_late',
            'assigned',
            'unexcused',
            'created_at',
            'updated_at',)
        read_only_fields = ('created_at', 'updated_at',)

    def create(self, validated_data):
        check_in_time = validated_data.get('check_in_time', None)
        is_late = validated_data.pop('is_late', None)
        event_id = validated_data.get('event_id', None)
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

                points = calculate_attendance_points(
                    new_check_in_time,
                    event,
                    validated_data.get('unexcused', None),
                    validated_data.get('assigned', None))
                validated_data['check_in_time'] = new_check_in_time
                validated_data['points'] = points
        else:
            validated_data['check_in_time'] = None
            validated_data['points'] = event.points

        attendance = Attendance.objects.create(**validated_data)
        return attendance

    def update(self, instance, validated_data):
        check_in_time = validated_data.get('check_in_time', None)
        is_late = validated_data.pop('is_late', None)
        event = instance.event
        assigned = validated_data.get('assigned', None)
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

        Attendance.objects.filter(id=instance.id).update(**validated_data)
        attendance = Attendance.objects.get(id=instance.id)
        return attendance
