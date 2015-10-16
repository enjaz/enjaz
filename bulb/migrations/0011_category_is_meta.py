# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bulb', '0010_typo_modification'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_meta',
            field=models.BooleanField(default=False, verbose_name='\u062a\u0635\u0646\u064a\u0641 \u0639\u0644\u0648\u064a\u061f'),
        ),
    ]
