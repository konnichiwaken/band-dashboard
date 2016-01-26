# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0005_attendance_assigned'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='unexcused',
            field=models.BooleanField(default=False, verbose_name=b'Unexcused absence'),
        ),
    ]
