# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0022_add_time_n_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='casereport',
            name='who_deleted',
            field=models.ForeignKey(related_name='deleted_casereports', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='casereport',
            name='why_deleted',
            field=models.TextField(default=b'', verbose_name='Justification for Deletion', blank=True),
        ),
    ]
