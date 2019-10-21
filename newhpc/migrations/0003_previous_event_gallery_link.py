# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newhpc', '0002_editing_previouse_versions_models'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gallery',
            name='show_more',
        ),
        migrations.AddField(
            model_name='previousversion',
            name='show_more',
            field=models.URLField(default=b'', verbose_name=b'Gallery Show more pictures link', blank=True),
        ),
    ]
