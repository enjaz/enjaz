# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matching_program', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='researchproject',
            name='field',
            field=models.CharField(max_length=255, null=True, verbose_name=b'field'),
        ),
    ]
