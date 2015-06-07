# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='club',
            name='special',
        ),
        migrations.AddField(
            model_name='club',
            name='can_review',
            field=models.BooleanField(default=False, verbose_name='\u064a\u0633\u062a\u0637\u064a\u0639 \u0627\u0644\u0645\u0631\u0627\u062c\u0639\u0629\u061f'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='club',
            name='visible',
            field=models.BooleanField(default=True, verbose_name='\u0645\u0631\u0626\u064a\u061f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='club',
            name='parent',
            field=models.ForeignKey(related_name='children', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='clubs.Club', null=True, verbose_name='\u0627\u0644\u0646\u0627\u062f\u064a \u0627\u0644\u0623\u0628'),
            preserve_default=True,
        ),
    ]
