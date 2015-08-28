# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0002_buzz_buzzview'),
    ]

    operations = [
        migrations.AddField(
            model_name='buzz',
            name='is_push',
            field=models.BooleanField(default=False, verbose_name='\u0625\u0639\u0644\u0627\u0646 \u0639\u0627\u0645\u061f'),
        ),
    ]
