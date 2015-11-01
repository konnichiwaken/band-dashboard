# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BandMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('section', models.CharField(max_length=255, verbose_name=b'Section', choices=[(b'bass', b'Bass'), (b'clarinet', b'Clarinet'), (b'drumline', b'Drumline'), (b'flute', b'Flute'), (b'mellophone', b'Mellophone'), (b'saxophone', b'Saxophone'), (b'trombone', b'Trombone'), (b'trumpet', b'Trumpet')])),
                ('instrument_number', models.IntegerField(null=True, verbose_name=b'Instrument number')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('account', models.OneToOneField(related_name='band_member', verbose_name=b'Account', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
