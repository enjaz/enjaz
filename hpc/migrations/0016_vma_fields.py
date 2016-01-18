# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hpc', '0015_registration_is_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='was_moved_to_vma',
            field=models.BooleanField(default=False, verbose_name='\u0646\u0642\u0644 \u0625\u0644\u0649 \u0627\u0644\u0623\u0643\u0627\u062f\u064a\u0645\u064a\u0629\u061f'),
        ),
        migrations.AddField(
            model_name='session',
            name='vma_time_code',
            field=models.PositiveSmallIntegerField(default=None, null=True, blank=True),
        ),
    ]
