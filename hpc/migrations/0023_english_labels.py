# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hpc', '0022_optional_arabic_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nonuser',
            name='en_first_name',
            field=models.CharField(max_length=30, verbose_name=b'First name'),
        ),
        migrations.AlterField(
            model_name='nonuser',
            name='en_last_name',
            field=models.CharField(max_length=30, verbose_name=b'Last name'),
        ),
        migrations.AlterField(
            model_name='nonuser',
            name='en_middle_name',
            field=models.CharField(max_length=30, verbose_name=b'Middle name'),
        ),
    ]
