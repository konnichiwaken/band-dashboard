from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers

from authentication.models import Account
from members.models import Band
from members.models import BandMember
from members.serializers import BandMemberSerializer


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)
    band_member = BandMemberSerializer()
    roles = serializers.StringRelatedField(many=True, required=False)

    class Meta:
        model = Account
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'created_at',
            'updated_at',
            'password',
            'confirm_password',
            'band_member',
            'roles',
            'is_registered',
        )
        read_only_fields = ('created_at', 'updated_at',)

    def create(self, validated_data):
        band_member_data = validated_data.pop('band_member')
        account = Account.objects.create_user(**validated_data)
        band_member = BandMember.objects.create(account=account, **band_member_data)
        for band in Band.objects.all():
            band.unassigned_members.add(band_member)
            band.save()

        return account

    def update(self, instance, validated_data):
        password = validated_data.get('password', None)
        confirm_password = validated_data.get('confirm_password', None)

        if password and confirm_password and password == confirm_password:
            instance.set_password(password)
            instance.save()

        update_session_auth_hash(self.context.get('request'), instance)
        return instance
