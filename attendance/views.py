import json

from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework import views
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from attendance.models import Attendance
from attendance.models import Event
from attendance.models import EventType
from attendance.permissions import IsAttendanceAdmin
from attendance.permissions import IsAttendanceAdminOrReadOnly
from attendance.serializers import AttendanceSerializer
from attendance.serializers import EventSerializer
from attendance.serializers import EventTypeSerializer
from attendance.utils import is_attendance_admin
from members.models import BandMember


class EventTypeViewSet(viewsets.ModelViewSet):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer
    permission_classes = (IsAuthenticated, IsAttendanceAdminOrReadOnly,)


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated, IsAttendanceAdminOrReadOnly,)

    def get_queryset(self):
        queryset = Event.objects.all()
        event_id = self.request.query_params.get('id', None)
        if event_id:
            queryset = queryset.filter(id=event_id)

        return queryset


class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = (IsAuthenticated, IsAttendanceAdminOrReadOnly,)

    def get_queryset(self):
        queryset = Attendance.objects.filter(is_active=True)
        event_id = self.request.query_params.get('event_id', None)
        if event_id:
            queryset = queryset.filter(event_id=event_id)

        account = self.request.user
        if not is_attendance_admin(account):
            queryset = queryset.filter(member__account=account)

        return queryset


class UnassignedAttendanceView(views.APIView):
    permission_classes = (IsAuthenticated, IsAttendanceAdmin,)

    def post(self, request, format=None):
        data = json.loads(request.body)
        serializer = AttendanceSerializer(data=data)
        if serializer.is_valid():
            attendance = serializer.save()
            return Response(model_to_dict(attendance), status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

class GetUnassignedMembersView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        account = self.request.user
        event_id = self.request.query_params.get('event_id')
        event = Event.objects.get(id=event_id)
        assignable_members = BandMember.objects.exclude(id=account.band_member.id)
        if event.band:
            assigned_members = event.band.assigned_members.values_list("id", flat=True)
            assignable_members = assignable_members.exclude(id__in=assigned_members)

        section = account.band_member.section
        assignable_members = assignable_members.filter(section=section)
        assignable_acounts = [member.account for member in assignable_members]
        return Response(
            {
                'full_name': account.get_full_name(),
                'id': account.id,
            } for account in assignable_acounts)

class SubstitutionFormView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        data = json.loads(request.body)
        print data
        return Response()
