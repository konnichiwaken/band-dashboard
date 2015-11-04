# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_auto_20151103_0757'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='type',
            field=models.ForeignKey(related_name='events', default=None, verbose_name=b'Event type', to='attendance.EventType'),
            preserve_default=False,
        ),
    ]
