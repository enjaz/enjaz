# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hpc', '0004_evaluation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstract',
            name='college',
            field=models.CharField(max_length=255, verbose_name=b'College'),
        ),
        migrations.AlterField(
            model_name='abstract',
            name='phone',
            field=models.CharField(max_length=20, verbose_name=b'Phone number'),
        ),
        migrations.AlterField(
            model_name='abstract',
            name='presentation_preference',
            field=models.CharField(max_length=1, verbose_name=b'Presentation preference', choices=[(b'O', b'Oral'), (b'P', b'Poster')]),
        ),
        migrations.AlterField(
            model_name='abstract',
            name='presenting_author',
            field=models.CharField(max_length=255, verbose_name=b'Presenting author'),
        ),
        migrations.AlterField(
            model_name='abstract',
            name='title',
            field=models.CharField(max_length=255, verbose_name=b'Title'),
        ),
        migrations.AlterField(
            model_name='abstract',
            name='university',
            field=models.CharField(max_length=255, verbose_name=b'University'),
        ),
    ]
