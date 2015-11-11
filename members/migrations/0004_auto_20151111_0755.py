# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_auto_20151111_0738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bandmember',
            name='band',
            field=models.ManyToManyField(related_name='band_members', verbose_name=b'Band', to='members.Band'),
        ),
    ]
