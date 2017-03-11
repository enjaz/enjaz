# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0033_add case report'),
    ]

    operations = [
        migrations.AddField(
            model_name='abstract',
            name='evaluators',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='\u0627\u0644\u0645\u0642\u064a\u0645\u064a\u0646', blank=True),
        ),
    ]
