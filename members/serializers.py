from rest_framework import serializers

from members.models import Band
from members.models import BandMember


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


class BandMemberSerializer(serializers.ModelSerializer):
    bands = BandSerializer(many=True)

    class Meta:
        model = BandMember
        fields = ('id',
            'account',
            'full_name',
            'section',
            'instrument_number',
            'bands',
            'created_at',
            'updated_at',)
        read_only_fields = ('account', 'full_name', 'created_at', 'updated_at',)
