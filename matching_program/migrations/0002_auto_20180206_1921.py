# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('matching_program', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='researchproject',
            name='members',
            field=models.ManyToManyField(related_name='members', verbose_name=b'members', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
