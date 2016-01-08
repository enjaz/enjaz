# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hpc', '0010_add_more_hpc_sessions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='gender',
            field=models.CharField(default=b'', max_length=1, blank=True, choices=[(b'', '\u0627\u0644\u062c\u0645\u064a\u0639'), (b'F', '\u0637\u0627\u0644\u0628\u0629'), (b'M', '\u0637\u0627\u0644\u0628')]),
        ),
        migrations.AlterField(
            model_name='session',
            name='limit',
            field=models.PositiveSmallIntegerField(default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='time_slot',
            field=models.PositiveSmallIntegerField(default=None, null=True, blank=True),
        ),
    ]
