# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clubs', '0032_fix_emails'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='media_representatives',
            field=models.ManyToManyField(related_name='media_representations', verbose_name='\u0627\u0644\u0645\u0645\u062b\u0644\u064a\u0646 \u0627\u0644 \u0627\u0644\u0625\u0639\u0644\u0627\u0645\u064a\u064a\u0646', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
