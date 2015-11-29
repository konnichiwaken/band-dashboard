from rest_framework import views
from rest_framework import viewsets
from rest_framework.response import Response

from members.models import Band
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
