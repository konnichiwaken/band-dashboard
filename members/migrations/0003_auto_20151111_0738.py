# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_auto_20151103_0757'),
    ]

    operations = [
        migrations.AddField(
            model_name='band',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 11, 7, 38, 41, 867723, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='band',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 11, 7, 38, 47, 147434, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='bandmember',
            name='band',
        ),
        migrations.AddField(
            model_name='bandmember',
            name='band',
            field=models.ManyToManyField(related_name='band_members', null=True, verbose_name=b'Band', to='members.Band'),
        ),
    ]
