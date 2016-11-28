# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0030_auto_20161124_1930'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invitation',
            name='registered_students',
        ),
    ]
