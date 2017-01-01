# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0032_invitation_club'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='notes',
            field=models.TextField(null=True, verbose_name='\u0648\u0635\u0641 \u0645\u0637\u0648\u0644', blank=True),
        ),
    ]
