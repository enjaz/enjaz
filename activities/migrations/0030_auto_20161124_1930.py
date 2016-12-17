# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0029_auto_20161124_1915'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invitation',
            old_name='is_open_regestration',
            new_name='is_open_registration',
        ),
    ]
