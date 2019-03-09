# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tedx', '0006_add_work_place_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='attended',
            field=models.BooleanField(default=False, verbose_name='\u0647\u0644 \u062d\u0636\u0631 \u0627\u0644\u062d\u062f\u062b\u061f'),
        ),
        migrations.AddField(
            model_name='registration',
            name='registration_user',
            field=models.ForeignKey(related_name='registrations_attendance_user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
