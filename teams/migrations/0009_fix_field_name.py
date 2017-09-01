# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0008_del_original_members'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='members2',
            new_name='members',
        ),
    ]
