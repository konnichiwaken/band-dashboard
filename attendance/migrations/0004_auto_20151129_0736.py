# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0003_event_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name=b'Is active'),
        ),
        migrations.AlterField(
            model_name='event',
            name='band',
            field=models.ForeignKey(related_name='events', verbose_name=b'Band', to='members.Band', null=True),
        ),
    ]
