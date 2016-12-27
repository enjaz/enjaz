# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activities', '0027_invitation_maximum_registrants'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='is_open_regestration',
            field=models.BooleanField(default=True, verbose_name='\u0646\u0634\u0627\u0637 \u0645\u0641\u062a\u0648\u062d \u061f'),
        ),
        migrations.AddField(
            model_name='invitation',
            name='registered_students',
            field=models.ManyToManyField(related_name='registered', verbose_name='\u0627\u0644\u0645\u0633\u062c\u0644\u0646', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
