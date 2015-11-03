# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Band',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(max_length=255, verbose_name=b'Band identifier')),
            ],
        ),
        migrations.AddField(
            model_name='bandmember',
            name='band',
            field=models.ForeignKey(related_name='band_members', verbose_name=b'Band', to='members.Band', null=True),
        ),
    ]
