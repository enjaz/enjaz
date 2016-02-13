# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('researchhub', '0003_improve_model_layout'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supervisor',
            name='position',
        ),
    ]
