# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hpc_temp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hpcperson',
            name='hpc_version',
            field=models.ManyToManyField(related_name='version_personnel', verbose_name='\u0627\u0644\u0646\u0633\u062e\u0629', to='hpc_temp.HPCVersion', blank=True),
        ),
    ]
