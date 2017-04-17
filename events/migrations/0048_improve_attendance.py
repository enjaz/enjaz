# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0047_add_hpc2_attendance_team'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='session',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='user',
        ),
        migrations.AddField(
            model_name='attendance',
            name='session_registration',
            field=models.ForeignKey(verbose_name='\u0627\u0644\u062a\u0633\u062c\u064a\u0644', to='events.SessionRegistration', null=True),
        ),
        migrations.AddField(
            model_name='attendance',
            name='submitter',
            field=models.ForeignKey(related_name='submitted_attendance', verbose_name='\u0627\u0644\u0645\u064f\u062f\u062e\u0644\u0640/\u0640\u0629', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
