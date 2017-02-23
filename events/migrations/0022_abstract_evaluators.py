# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0021_abstract_previous_participation_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='abstract',
            name='evaluators',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='\u0627\u0644\u0645\u0642\u064a\u0645\u064a\u0646', blank=True),
        ),
    ]
