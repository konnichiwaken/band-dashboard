# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_auto_20151129_0736'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='assigned',
            field=models.BooleanField(default=True, verbose_name=b'Assigned to event'),
            preserve_default=False,
        ),
    ]
