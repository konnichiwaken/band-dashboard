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
from attendance.models import SubstitutionForm
from attendance.permissions import IsAttendanceAdmin
from attendance.permissions import IsAttendanceAdminOrReadOnly
from attendance.serializers import AttendanceSerializer
from attendance.serializers import EventSerializer
from attendance.serializers import EventTypeSerializer
from attendance.serializers import SubstitutionFormSerializer
from attendance.utils import is_attendance_admin
from emails.utils import send_substitution_form_email
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
        try:
            member_id = data.get('member_id')
            event_id = data.get('event_id')
            attendance = Attendance.objects.get(member_id=member_id, event_id=event_id)
            data['is_active'] = True
            serializer = AttendanceSerializer()
            attendance = serializer.update(attendance, data)
            return Response(model_to_dict(attendance))
        except Attendance.DoesNotExist:
            serializer = AttendanceSerializer(data=data)
            if serializer.is_valid():
                attendance = serializer.save()
                return Response(model_to_dict(attendance))

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
                'id': account.band_member.id,
            } for account in assignable_acounts)


class SubstitutionFormViewSet(viewsets.ModelViewSet):
    serializer_class = SubstitutionFormSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        data = request.data
        data['requester'] = request.user.band_member.id
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            validated_data = serializer.validated_data
            send_substitution_form_email(
                validated_data['event'],
                validated_data['requestee'],
                validated_data['requester'])
            return_data = {
                'event_id': validated_data['event'].id,
                'reason': validated_data['reason'],
                'requestee_id': validated_data['requestee'].id,
                'requester_id': validated_data['requester'].id,
            }

            return Response(return_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.',
        }, status=status.HTTP_400_BAD_REQUEST)


class GetPendingSubstitutionForms(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        requested_substitution_forms = SubstitutionForm.objects.filter(
            status=SubstitutionForm.PENDING,
            requester=request.user.band_member).values(
            'event__time',
            'event__title',
            'id',
            'reason',
            'requestee__account__first_name',
            'requestee__account__last_name')
        received_substitution_forms = SubstitutionForm.objects.filter(
            status=SubstitutionForm.PENDING,
            requestee=request.user.band_member).values(
            'event__time',
            'event__title',
            'id',
            'requester__account__first_name',
            'requester__account__last_name')

        return Response({
            'requested': requested_substitution_forms,
            'received': received_substitution_forms,
        })


class AcceptSubstitutionForm(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = json.loads(request.body)
        substitution_form_id = data['substitutionForm']
        try:
            substitution_form = SubstitutionForm.objects.get(
                id=substitution_form_id,
                requestee_id=request.user.band_member.id)
            substitution_form.accept()
            return Response({})
        except SubstitutionForm.DoesNotExist:
            return Response({
                'status': 'Bad request',
                'message': 'Could not accept substitution form with given information',
            }, status=status.HTTP_400_BAD_REQUEST)


class DeclineSubstitutionForm(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = json.loads(request.body)
        substitution_form_id = data['substitutionForm']
        try:
            substitution_form = SubstitutionForm.objects.get(
                id=substitution_form_id,
                requestee_id=request.user.band_member.id)
            substitution_form.decline()
            return Response({})
        except SubstitutionForm.DoesNotExist:
            return Response({
                'status': 'Bad request',
                'message': 'Could not decline substitution form with given information',
            }, status=status.HTTP_400_BAD_REQUEST)
