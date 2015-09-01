# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clubs', '0033_club_media_representatives'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='media_assessor',
            field=models.ForeignKey(related_name='media_assessments', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u0627\u0644\u0645\u064f\u0642\u064a\u0651\u0645 \u0627\u0644\u0625\u0639\u0644\u0627\u0645\u064a'),
        ),
    ]
