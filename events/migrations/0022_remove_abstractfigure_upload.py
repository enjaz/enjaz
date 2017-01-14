# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0021_abstract_previous_participation_fields'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='abstractfigure',
            name='upload',
        ),
    ]
