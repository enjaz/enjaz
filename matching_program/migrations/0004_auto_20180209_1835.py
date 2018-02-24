# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('matching_program', '0003_auto_20180209_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='researchproject',
            name='creator',
            field=models.ForeignKey(related_name='creator', to=settings.AUTH_USER_MODEL),
        ),
    ]
