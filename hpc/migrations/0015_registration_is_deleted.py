# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hpc', '0014_blank_code_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='\u0645\u062d\u0630\u0648\u0641\u061f'),
        ),
    ]
