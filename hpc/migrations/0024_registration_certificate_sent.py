# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hpc', '0023_english_labels'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='certificate_sent',
            field=models.BooleanField(default=False, verbose_name='\u0623\u0631\u0633\u0644\u062a \u0627\u0644\u0634\u0647\u0627\u062f\u0629\u061f'),
        ),
    ]
