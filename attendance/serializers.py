from rest_framework import serializers

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
