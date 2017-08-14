# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('approvals', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activityrequest',
            name='description',
        ),
        migrations.AlterField(
            model_name='activityrequest',
            name='name',
            field=models.CharField(max_length=200, verbose_name='\u0627\u0644\u0639\u0646\u0648\u0627\u0646'),
        ),
        migrations.AlterField(
            model_name='eventrequest',
            name='date',
            field=models.DateField(verbose_name='\u0627\u0644\u062a\u0627\u0631\u064a\u062e'),
        ),
        migrations.AlterField(
            model_name='eventrequest',
            name='description',
            field=models.CharField(max_length=200, verbose_name='\u0627\u0644\u0648\u0635\u0641'),
        ),
        migrations.AlterField(
            model_name='eventrequest',
            name='end_time',
            field=models.TimeField(verbose_name='\u0648\u0642\u062a \u0627\u0644\u0646\u0647\u0627\u064a\u0629'),
        ),
        migrations.AlterField(
            model_name='eventrequest',
            name='label',
            field=models.CharField(max_length=50, verbose_name='\u0627\u0644\u0639\u0646\u0648\u0627\u0646'),
        ),
        migrations.AlterField(
            model_name='eventrequest',
            name='location',
            field=models.CharField(max_length=50, verbose_name='\u0627\u0644\u0645\u0643\u0627\u0646'),
        ),
        migrations.AlterField(
            model_name='eventrequest',
            name='start_time',
            field=models.TimeField(verbose_name='\u0648\u0642\u062a \u0627\u0644\u0628\u062f\u0627\u064a\u0629'),
        ),
    ]
