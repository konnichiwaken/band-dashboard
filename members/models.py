from django.db import models

from authentication.models import Account


class Band(models.Model):
    identifier = models.CharField(max_length=255, verbose_name='Band identifier')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BandMember(models.Model):
    BASS = 'bass'
    CLARINET = 'clarinet'
    DRUMLINE = 'drumline'
    FLUTE = 'flute'
    MELLOPHONE = 'mellophone'
    SAXOPHONE = 'saxophone'
    TROMBONE = 'trombone'
    TRUMPET = 'trumpet'
    SECTION_CHOICES = (
        (BASS, 'Bass'),
        (CLARINET, 'Clarinet'),
        (DRUMLINE, 'Drumline'),
        (FLUTE, 'Flute'),
        (MELLOPHONE, 'Mellophone'),
        (SAXOPHONE, 'Saxophone'),
        (TROMBONE, 'Trombone'),
        (TRUMPET, 'Trumpet'),
    )
    account = models.OneToOneField(Account, related_name='band_member', verbose_name='Account')
    section = models.CharField(max_length=255, choices=SECTION_CHOICES, verbose_name='Section')
    instrument_number = models.IntegerField(null=True, verbose_name='Instrument number')
    band = models.ManyToManyField(Band, related_name='band_members', verbose_name='Band')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
