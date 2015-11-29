import json

from rest_framework import views
from rest_framework import viewsets
from rest_framework.response import Response

from members.models import Band
from members.models import BandMember
from members.serializers import BandSerializer


class BandViewSet(viewsets.ModelViewSet):
    queryset = Band.objects.all()
    serializer_class = BandSerializer


class BandAssignmentView(views.APIView):

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
                    "section": assigned_member.section
                }
                member_assignments["assigned"].append(member_assignment)

            for unassigned_member in band.unassigned_members.all():
                member_assignment = {
                    "id": unassigned_member.id,
                    "name": unassigned_member.full_name,
                    "section": unassigned_member.section
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
            elif action =='unassign':
                band.unassigned_members.add(band_member)
                band.assigned_members.remove(band_member)

            band.save()

        return Response()
