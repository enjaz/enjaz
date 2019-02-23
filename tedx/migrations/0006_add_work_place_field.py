# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tedx', '0005_null_old_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='work_place',
            field=models.CharField(max_length=50, null=True, verbose_name='\u0645\u0643\u0627\u0646 \u0627\u0644\u0639\u0645\u0644 \u0627\u0648 \u0627\u0644\u062f\u0631\u0627\u0633\u0629', blank=True),
        ),
    ]
