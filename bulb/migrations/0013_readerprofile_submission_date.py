# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bulb', '0012_add_all_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='readerprofile',
            name='submission_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644', null=True),
        ),
    ]
