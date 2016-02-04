# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0007_auto_20160203_0804'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='is_absence',
            field=models.BooleanField(default=False),
        ),
    ]
