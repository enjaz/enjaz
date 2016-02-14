# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_commonprofile_modification_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commonprofile',
            name='job_description',
            field=models.TextField(verbose_name='\u0627\u0644\u0645\u0633\u0645\u0649 \u0627\u0644\u0648\u0638\u064a\u0641\u064a', blank=True),
        ),
    ]
