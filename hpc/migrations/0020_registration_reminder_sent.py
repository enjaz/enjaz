# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hpc', '0019_registration_confirmation_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='reminder_sent',
            field=models.BooleanField(default=False, verbose_name='\u0623\u0631\u0633\u0644\u062a \u0631\u0633\u0627\u0644\u0629 \u0627\u0644\u062a\u0630\u0643\u064a\u0631\u061f'),
        ),
    ]
