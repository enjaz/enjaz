# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('researchhub', '0009_add_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='skilledstudent',
            name='fields_of_interest',
            field=models.CharField(default=b'', help_text=b'In what fields you are interested?', max_length=250),
        ),
    ]
