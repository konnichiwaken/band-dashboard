# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0006_auto_20160126_0639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='band',
            name='identifier',
            field=models.CharField(unique=True, max_length=255, verbose_name=b'Band identifier'),
        ),
    ]
