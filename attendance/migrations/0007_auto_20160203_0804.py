# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0006_attendance_unexcused'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='unexcused',
            field=models.NullBooleanField(verbose_name=b'Unexcused absence/late'),
        ),
    ]
