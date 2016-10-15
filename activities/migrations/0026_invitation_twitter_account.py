# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0025_city_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='twitter_account',
            field=models.CharField(default=b'', max_length=20, verbose_name='\u062d\u0633\u0627\u0628 \u062a\u0648\u064a\u062a\u0631', blank=True),
        ),
    ]
