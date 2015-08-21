# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('arshidni', '0003_auto_20150820_0738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colleagueprofile',
            name='user',
            field=models.ForeignKey(related_name='colleague_profile', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
