from rest_framework import serializers

from attendance.models import Event
from attendance.models import EventType
from members.models import Band
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
        return event
