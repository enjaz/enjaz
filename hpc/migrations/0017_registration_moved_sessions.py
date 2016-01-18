# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hpc', '0016_vma_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='moved_sessions',
            field=models.ManyToManyField(related_name='moved_registrations', to='hpc.Session', blank=True),
        ),
    ]
