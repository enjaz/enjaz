# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0004_reorganize_clubs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='deputies',
            field=models.ManyToManyField(related_name='deputyships', verbose_name='\u0627\u0644\u0646\u0648\u0627\u0628', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='club',
            name='members',
            field=models.ManyToManyField(related_name='memberships', verbose_name='\u0627\u0644\u0623\u0639\u0636\u0627\u0621', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
