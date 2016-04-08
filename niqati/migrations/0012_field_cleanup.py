# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('niqati', '0011_rename_models'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collection',
            old_name='code_category',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='collection',
            old_name='parent_order',
            new_name='order',
        ),
        migrations.RenameField(
            model_name='code',
            old_name='code_string',
            new_name='string',
        ),
        migrations.RemoveField(
            model_name='code',
            name='category',
        ),
    ]
