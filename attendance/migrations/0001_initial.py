# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('points', models.DecimalField(null=True, verbose_name=b'Points', max_digits=5, decimal_places=2)),
                ('check_in_time', models.DateTimeField(null=True, verbose_name=b'Check-in time')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name=b'Title')),
                ('time', models.DateTimeField(verbose_name=b'Date and time of event')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(unique=True, max_length=255, verbose_name=b'Event type')),
                ('points', models.DecimalField(verbose_name=b'Points', max_digits=5, decimal_places=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.ForeignKey(related_name='+', verbose_name=b'Event type', to='attendance.EventType'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='event',
            field=models.ForeignKey(related_name='attendances', verbose_name=b'Event', to='attendance.Event'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='member',
            field=models.ForeignKey(related_name='attendances', verbose_name=b'Band member', to='members.BandMember'),
        ),
    ]
