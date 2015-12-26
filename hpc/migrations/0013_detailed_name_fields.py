# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hpc', '0012_fix_gender_choices'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nonuser',
            name='ar_name',
        ),
        migrations.RemoveField(
            model_name='nonuser',
            name='en_name',
        ),
        migrations.AddField(
            model_name='nonuser',
            name='ar_first_name',
            field=models.CharField(default='', max_length=30, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0623\u0648\u0644'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nonuser',
            name='ar_last_name',
            field=models.CharField(default='', max_length=30, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0623\u062e\u064a\u0631'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nonuser',
            name='ar_middle_name',
            field=models.CharField(default='', max_length=30, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0623\u0648\u0633\u0637'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nonuser',
            name='en_first_name',
            field=models.CharField(default='', max_length=30, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0623\u0648\u0644'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nonuser',
            name='en_last_name',
            field=models.CharField(default='', max_length=30, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0623\u062e\u064a\u0631'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nonuser',
            name='en_middle_name',
            field=models.CharField(default='', max_length=30, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0623\u0648\u0633\u0637'),
            preserve_default=False,
        ),
    ]
