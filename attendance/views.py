from rest_framework import viewsets

from attendance.models import Event
from attendance.models import EventType
from attendance.serializers import EventSerializer
from attendance.serializers import EventTypeSerializer


class EventTypeViewSet(viewsets.ModelViewSet):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

