# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studentguide', '0005_add_studentguide_clubs'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='image',
            field=models.FileField(null=True, upload_to=b'studentguide/tags/', blank=True),
        ),
    ]
