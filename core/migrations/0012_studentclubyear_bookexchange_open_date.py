# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_studentclubyear_bookexchange_close_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentclubyear',
            name='bookexchange_open_date',
            field=models.DateField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0641\u062a\u062d \u062a\u0628\u0627\u062f\u0644 \u0627\u0644\u0643\u062a\u0628', blank=True),
        ),
    ]
