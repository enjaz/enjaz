# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0047_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='logo',
            field=models.ImageField(null=True, upload_to=b'invitations/logos/', blank=True),
        ),
    ]
