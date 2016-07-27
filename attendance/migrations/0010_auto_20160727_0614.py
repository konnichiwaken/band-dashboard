# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0009_substitutionform'),
    ]

    operations = [
        migrations.AddField(
            model_name='substitutionform',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 27, 6, 14, 38, 395979, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='substitutionform',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 27, 6, 14, 45, 36472, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
