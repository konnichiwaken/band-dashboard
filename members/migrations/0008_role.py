# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('members', '0007_auto_20160204_0631'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name=b'Role name')),
                ('accounts', models.ManyToManyField(related_name='roles', verbose_name=b'Accounts with role', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
    ]
