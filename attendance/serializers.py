from rest_framework import serializers

from attendance.models import Event
from attendance.models import EventType


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

    class Meta:
        model = Event
        fields = ('id',
            'title',
            'created_at',
            'updated_at',
            'time',
            'type',
            'band',
            'points',
            'ready_to_play',)
        read_only_fields = ('created_at', 'updated_at',)
