from rest_framework import viewsets

from attendance.models import Attendance
from attendance.models import Event
from attendance.models import EventType
from attendance.serializers import AttendanceSerializer
from attendance.serializers import EventSerializer
from attendance.serializers import EventTypeSerializer


class EventTypeViewSet(viewsets.ModelViewSet):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = Event.objects.all()
        event_id = self.request.query_params.get('id', None)
        if event_id:
            queryset = queryset.filter(id=event_id)

        return queryset


class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        queryset = Attendance.objects.filter(is_active=True)
        event_id = self.request.query_params.get('event_id', None)
        if event_id:
            queryset = queryset.filter(event_id=event_id)

        return queryset
