# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_campus_specialty'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Announcement',
        ),
    ]
