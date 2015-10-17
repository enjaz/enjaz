# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bulb', '0009_add_others_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='modifiation_date',
            new_name='modification_date',
        ),
        migrations.RenameField(
            model_name='group',
            old_name='modifiation_date',
            new_name='modification_date',
        ),
        migrations.RenameField(
            model_name='membership',
            old_name='modifiation_date',
            new_name='modification_date',
        ),
    ]
