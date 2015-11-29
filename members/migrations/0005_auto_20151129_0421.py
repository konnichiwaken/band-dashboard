# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_auto_20151111_0755'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bandmember',
            name='band',
        ),
        migrations.AddField(
            model_name='band',
            name='assigned_members',
            field=models.ManyToManyField(related_name='bands', verbose_name=b'Assigned members', to='members.BandMember'),
        ),
        migrations.AddField(
            model_name='band',
            name='unassigned_members',
            field=models.ManyToManyField(related_name='_unassigned_members_+', verbose_name=b'Unassigned members', to='members.BandMember'),
        ),
    ]
