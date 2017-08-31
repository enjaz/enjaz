# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0007_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='followupreport',
            name='is_draft',
            field=models.BooleanField(default=False, verbose_name='\u062d\u0641\u0638 \u0643\u0645\u0633\u0648\u062f\u0629'),
        ),
    ]
