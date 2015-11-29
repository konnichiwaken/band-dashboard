from rest_framework import serializers

from members.models import Band
from members.models import BandMember


class BandMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = BandMember
        fields = ('id',
            'account',
            'section',
            'instrument_number',
            'band',
            'created_at',
            'updated_at',)
        read_only_fields = ('account', 'created_at', 'updated_at',)


class BandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Band
        fields = ('id',
            'identifier',
            'created_at',
            'updated_at',)
        read_only_fields = ('created_at', 'updated_at',)

    def create(self, validated_data):
        band = Band.objects.create(**validated_data)
        band.unassigned_members = BandMember.objects.all()
        band.save()
        return band
