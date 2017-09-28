# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0009_snapchat'),
    ]

    operations = [
        migrations.AddField(
            model_name='snapchat',
            name='pup_date',
            field=models.DateField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0637\u0644\u0628', null=True),
        ),
        migrations.AlterField(
            model_name='snapchat',
            name='date',
            field=models.DateField(verbose_name='\u0627\u0644\u062a\u0627\u0631\u064a\u062e'),
        ),
        migrations.AlterField(
            model_name='snapchat',
            name='end_time',
            field=models.TimeField(default=b'24:00', verbose_name='\u0648\u0642\u062a \u0627\u0644\u0646\u0647\u0627\u064a\u0629'),
        ),
        migrations.AlterField(
            model_name='snapchat',
            name='start_time',
            field=models.TimeField(default=b'12:00', verbose_name='\u0648\u0642\u062a \u0627\u0644\u0628\u062f\u0627\u064a\u0629'),
        ),
    ]
