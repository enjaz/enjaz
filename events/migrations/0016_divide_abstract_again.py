# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_add_user_to_abstract'),
    ]

    operations = [
        migrations.AddField(
            model_name='abstract',
            name='conclusion',
            field=models.TextField(default=b'', verbose_name='Conclusion'),
        ),
        migrations.AddField(
            model_name='abstract',
            name='discussion',
            field=models.TextField(default=b'', verbose_name='Discussion'),
        ),
        migrations.AddField(
            model_name='abstract',
            name='methodology',
            field=models.TextField(default=b'', verbose_name='Methodology'),
        ),
        migrations.AddField(
            model_name='abstract',
            name='results',
            field=models.TextField(default=b'', verbose_name='Results'),
        ),
    ]
