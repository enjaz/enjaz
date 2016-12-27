# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0048_club_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='logo',
            field=models.ImageField(null=True, upload_to=b'clubs/logos/', blank=True),
        ),
    ]
