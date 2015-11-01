from django.db import models

from authentication.models import Account


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
