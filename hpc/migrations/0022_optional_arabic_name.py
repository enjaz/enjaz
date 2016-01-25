# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hpc', '0021_session_for_onsite_registration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nonuser',
            name='ar_first_name',
            field=models.CharField(default=b'', max_length=30, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0623\u0648\u0644', blank=True),
        ),
        migrations.AlterField(
            model_name='nonuser',
            name='ar_last_name',
            field=models.CharField(default=b'', max_length=30, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0623\u062e\u064a\u0631', blank=True),
        ),
        migrations.AlterField(
            model_name='nonuser',
            name='ar_middle_name',
            field=models.CharField(default=b'', max_length=30, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0623\u0648\u0633\u0637', blank=True),
        ),
    ]
