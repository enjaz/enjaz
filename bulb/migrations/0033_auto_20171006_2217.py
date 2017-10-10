# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulb', '0032_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='recruitment',
            name='khamisia_guests',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='recruitment',
            name='khamisia_subjects',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='recruitment',
            name='wants_khamisia_organization',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='recruitment',
            name='wants_readathon_organization',
            field=models.BooleanField(default=False),
        ),
    ]
