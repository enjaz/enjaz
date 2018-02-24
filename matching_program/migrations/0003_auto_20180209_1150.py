# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matching_program', '0002_auto_20180206_1921'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='researchproject',
            name='field',
        ),
        migrations.AddField(
            model_name='researchproject',
            name='field',
            field=models.ForeignKey(verbose_name=b'field', to='matching_program.Field', null=True),
        ),
    ]
