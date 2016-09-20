import json

from django.forms import model_to_dict
from rest_framework import views
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from attendance.models import Attendance
from attendance.models import Event
from attendance.permissions import IsAttendanceAdmin
from attendance.permissions import IsAttendanceAdminOrReadOnly
from authentication.models import Account
from authentication.permissions import IsAccountAdminOrAccountOwner
from members.models import Band
from members.models import BandMember
from members.serializers import BandMemberSerializer
from members.serializers import BandSerializer


class BandViewSet(viewsets.ModelViewSet):
    queryset = Band.objects.all()
    serializer_class = BandSerializer
    permission_classes = (IsAuthenticated, IsAttendanceAdminOrReadOnly,)


class BandAssignmentView(views.APIView):
    permission_classes = (IsAuthenticated, IsAttendanceAdminOrReadOnly,)

    def get(self, request, format=None):
        band_assignments = {}
        for band in Band.objects.all():
            member_assignments = {}
            member_assignments["assigned"] = []
            member_assignments["unassigned"] = []
            for assigned_member in band.assigned_members.all():
                member_assignment = {
                    "id": assigned_member.id,
                    "name": assigned_member.full_name,
                    "section": assigned_member.section_display
                }
                member_assignments["assigned"].append(member_assignment)

            for unassigned_member in band.unassigned_members.all():
                member_assignment = {
                    "id": unassigned_member.id,
                    "name": unassigned_member.full_name,
                    "section": unassigned_member.section_display
                }
                member_assignments["unassigned"].append(member_assignment)

            band_assignments[band.id] = member_assignments

        return Response(band_assignments)


    def post(self, request, format=None):
        data = json.loads(request.body)
        member_id = data.get('member', None)
        band_id = data.get('band', None)
        action = data.get('action', None)
        if member_id and band_id and action:
            band_member = BandMember.objects.get(id=member_id)
            band = Band.objects.get(id=band_id)
            if action == 'assign':
                band.unassigned_members.remove(band_member)
                band.assigned_members.add(band_member)
                for event in band.events.all():
                    try:
                        attendance = Attendance.objects.get(event=event, member=band_member)
                        if attendance.points is None:
                            is_modified = False
                            if not attendance.assigned:
                                attendance.assigned = True
                                is_modified = True

                            if not attendance.is_active:
                                attendance.is_active = True
                                is_modified = True

                            if is_modified:
                                attendance.save()
                    except Attendance.DoesNotExist:
                        Attendance.objects.create(event=event, member=band_member, assigned=True)
            elif action == 'unassign':
                band.unassigned_members.add(band_member)
                band.assigned_members.remove(band_member)
                for event in band.events.all():
                    try:
                        attendance = Attendance.objects.get(
                            event=event,
                            member=band_member,
                            points__isnull=True,
                            assigned=True)
                        attendance.assigned = False
                        attendance.is_active = False
                        attendance.save()
                    except Attendance.DoesNotExist:
                        pass

            band.save()
            return Response()
        else:
            return Response({
                'status': 'Bad request',
                'message': 'Missing parameter in request',
            }, status=status.HTTP_400_BAD_REQUEST)


class BandMemberViewSet(viewsets.ModelViewSet):
    queryset = BandMember.objects.all()
    serializer_class = BandMemberSerializer
    permission_classes = (IsAuthenticated, IsAccountAdminOrAccountOwner,)


class UnassignedMembersView(views.APIView):
    permission_classes = (IsAuthenticated, IsAttendanceAdmin,)

    def get(self, request, format=None):
        event_id = self.request.query_params.get('event_id', None)
        if event_id:
            try:
                event = Event.objects.get(id=event_id)
            except Event.DoesNotExist:
                return Response({
                    'status': 'Bad request',
                    'message': 'Could not find event from event_id',
                }, status=status.HTTP_400_BAD_REQUEST)

            existing_unassigned_members = Attendance.objects.filter(
                event=event,
                assigned=False,
                is_active=True,
            ).values_list('member_id', flat=True).distinct()
            band = event.band
            if band:
                unassigned_members_queryset = band.unassigned_members
            else:
                unassigned_members_queryset = BandMember.objects.filter(account__is_active=True)

            unassigned_members = unassigned_members_queryset.exclude(
                id__in=existing_unassigned_members).all()
            unassigned_members_dicts = []
            for unassigned_member in unassigned_members:
                full_name = unassigned_member.full_name
                member_dict = model_to_dict(unassigned_member)
                member_dict['full_name'] = full_name
                unassigned_members_dicts.append(member_dict)

            return Response(unassigned_members_dicts)

        return Response({
            'status': 'Bad request',
            'message': 'No event_id in request',
        }, status=status.HTTP_400_BAD_REQUEST)
