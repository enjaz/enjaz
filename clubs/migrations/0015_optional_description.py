# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0014_fix_gender_verbose_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='description',
            field=models.TextField(verbose_name='\u0627\u0644\u0648\u0635\u0641', blank=True),
        ),
    ]
