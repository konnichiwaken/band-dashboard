from rest_framework import viewsets

from members.models import Band
from members.serializers import BandSerializer


class BandViewSet(viewsets.ModelViewSet):
    queryset = Band.objects.all()
    serializer_class = BandSerializer
