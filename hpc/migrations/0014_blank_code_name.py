# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hpc', '0013_detailed_name_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='code_name',
            field=models.CharField(default=b'', help_text='\u062d\u0631\u0648\u0641 \u0644\u0627\u062a\u064a\u0646\u064a\u0629 \u0635\u063a\u064a\u0631\u0629 \u0648\u0623\u0631\u0642\u0627\u0645', max_length=50, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0628\u0631\u0645\u062c\u064a', blank=True),
        ),
    ]
