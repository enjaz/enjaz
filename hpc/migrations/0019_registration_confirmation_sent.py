# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hpc', '0018_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='confirmation_sent',
            field=models.BooleanField(default=False, verbose_name='\u0623\u0631\u0633\u0644\u062a \u0631\u0633\u0627\u0644\u0629 \u0627\u0644\u062a\u0623\u0643\u064a\u062f\u061f'),
        ),
    ]
