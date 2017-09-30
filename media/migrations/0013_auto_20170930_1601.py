# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0012_auto_20170930_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snapchatreservation',
            name='submission_datetime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0637\u0644\u0628', null=True),
        ),
    ]
