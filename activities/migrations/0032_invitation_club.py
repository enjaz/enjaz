# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0048_club_logo'),
        ('activities', '0031_remove_invitation_registered_students'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='club',
            field=models.ForeignKey(blank=True, to='clubs.Club', null=True),
        ),
    ]
