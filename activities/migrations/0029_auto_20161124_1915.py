# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0028_auto_20161124_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='students',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='\u0627\u0644\u0645\u0642\u0628\u0648\u0644\u064a\u0646', blank=True),
        ),
    ]
