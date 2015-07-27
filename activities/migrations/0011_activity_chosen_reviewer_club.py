# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0021_add_jeddah_ahsa_deanships'),
        ('activities', '0010_auto_20150727_0251'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='chosen_reviewer_club',
            field=models.ForeignKey(related_name='chosen_reviewer_activities', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0643\u0644\u064a\u0629 \u0627\u0644\u0645\u0631\u0627\u062c\u0639\u0629', blank=True, to='clubs.Club', null=True),
        ),
    ]
