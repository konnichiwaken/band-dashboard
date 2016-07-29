# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0010_auto_20160727_0614'),
    ]

    operations = [
        migrations.AddField(
            model_name='substitutionform',
            name='status',
            field=models.CharField(default=b'pending', max_length=255, verbose_name=b'Status', choices=[(b'accept', b'Accepted'), (b'decline', b'Declined'), (b'pending', b'Pending')]),
        ),
    ]
