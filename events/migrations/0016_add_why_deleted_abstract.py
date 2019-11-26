# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_edit_relationship'),
    ]

    operations = [
        migrations.AddField(
            model_name='abstract',
            name='why_deleted',
            field=models.TextField(default=b'', verbose_name='Justification for Deletion', blank=True),
        ),
    ]
