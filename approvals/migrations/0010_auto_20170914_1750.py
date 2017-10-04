# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0011_merge'),
        ('approvals', '0009_activityrequestcomment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activityrequestreview',
            options={'verbose_name': '\u0645\u0631\u0627\u062c\u064e\u0639\u0629', 'verbose_name_plural': '\u0645\u0631\u0627\u062c\u064e\u0639\u0627\u062a'},
        ),
        migrations.RemoveField(
            model_name='activityrequestreview',
            name='review_datetime',
        ),
        migrations.AddField(
            model_name='activityrequestreview',
            name='submission_datetime',
            field=models.DateTimeField(default=datetime.datetime(2017, 9, 14, 14, 50, 48, 411425, tzinfo=utc), verbose_name='\u0627\u0644\u062a\u0627\u0631\u064a\u062e \u0648 \u0627\u0644\u0648\u0642\u062a', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activityrequestreview',
            name='submitter',
            field=models.ForeignKey(related_name='activity_request_reviews', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u0631\u0627\u062c\u0650\u0639', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='activityrequestreview',
            name='submitter_team',
            field=models.ForeignKey(related_name='activity_request_reviews', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0641\u0631\u064a\u0642 \u0627\u0644\u0645\u0631\u0627\u062c\u0650\u0639', to='teams.Team', null=True),
        ),
    ]
