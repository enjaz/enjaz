# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0025_add_initiation'),
    ]

    operations = [
        migrations.RenameModel("InitiationFigure", "InitiativeFigure"),
        migrations.RenameModel("Initiation", "Initiative")
        ]
