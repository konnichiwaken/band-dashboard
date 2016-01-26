# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_auto_20151129_0421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='band',
            name='assigned_members',
            field=models.ManyToManyField(related_name='bands', verbose_name=b'Assigned members', to='members.BandMember', blank=True),
        ),
    ]
