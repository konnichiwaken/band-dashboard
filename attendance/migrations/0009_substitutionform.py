# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_role'),
        ('attendance', '0008_attendance_is_absence'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubstitutionForm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reason', models.CharField(max_length=255, verbose_name=b'Substitution reason')),
                ('event', models.ForeignKey(related_name='substitution_forms', verbose_name=b'Event', to='attendance.Event')),
                ('requestee', models.ForeignKey(related_name='substitutions_received', verbose_name=b'Requestee', to='members.BandMember')),
                ('requester', models.ForeignKey(related_name='substitutions_requested', verbose_name=b'Requester', to='members.BandMember')),
            ],
        ),
    ]
