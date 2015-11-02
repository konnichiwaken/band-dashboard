from rest_framework import serializers

from members.models import BandMember


class BandMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = BandMember
        fields = ('id',
            'account',
            'section',
            'instrument_number',
            'created_at',
            'updated_at',)
        read_only_fields = ('account', 'created_at', 'updated_at',)
