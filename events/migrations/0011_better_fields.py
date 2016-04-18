# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_onsite_after'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='is_on_telegram',
            field=models.BooleanField(default=True, verbose_name='\u0639\u0644\u0649 \u062a\u0644\u063a\u0631\u0627\u0645\u061f'),
        ),
        migrations.AlterField(
            model_name='event',
            name='onsite_after',
            field=models.DateField(null=True, verbose_name='\u0627\u0644\u062a\u0633\u062c\u064a\u0644 \u0641\u064a \u0627\u0644\u0645\u0648\u0642\u0639 \u064a\u0628\u062f\u0623 \u0645\u0646', blank=True),
        ),
    ]
