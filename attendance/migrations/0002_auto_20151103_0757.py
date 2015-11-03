# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_auto_20151103_0757'),
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='event_type',
        ),
        migrations.RemoveField(
            model_name='eventtype',
            name='type',
        ),
        migrations.AddField(
            model_name='event',
            name='band',
            field=models.ForeignKey(related_name='Events', verbose_name=b'Band', to='members.Band', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='points',
            field=models.DecimalField(default=0, verbose_name=b'Points', max_digits=5, decimal_places=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='ready_to_play',
            field=models.IntegerField(default=0, verbose_name=b'Minutes before event for RTP'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventtype',
            name='name',
            field=models.CharField(default='Hello', unique=True, max_length=255, verbose_name=b'Event type name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventtype',
            name='ready_to_play',
            field=models.IntegerField(default=0, verbose_name=b'Minutes before event for RTP'),
            preserve_default=False,
        ),
    ]
