# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0007_add_Membership'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='members',
        ),
    ]
