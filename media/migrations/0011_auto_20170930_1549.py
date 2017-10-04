# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0052_presidencies_can_assess'),
        ('media', '0010_auto_20170925_0229'),
    ]

    operations = [
        migrations.RenameModel(
            'Snapchat',
            'SnapchatReservation',
        )
    ]
