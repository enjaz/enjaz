# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('studentvoice', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipient',
            name='college',
            field=models.ManyToManyField(to='clubs.College', verbose_name='\u0627\u0644\u0643\u0644\u064a\u0629', blank=True),
        ),
        migrations.AlterField(
            model_name='recipient',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u0648\u0646', blank=True),
        ),
    ]
