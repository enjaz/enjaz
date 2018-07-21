# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0006_add_presenter_field_to_Session'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSurveyCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=1, choices=[(b'COM', '\u0643\u0644\u064a\u0629 \u0627\u0644\u0637\u0628'), (b'COD', '\u062e\u064a\u0627\u0631\u0627\u062a'), (b'COAMS', '\u0627\u0644\u0639\u0644\u0648\u0645 \u0627\u0644\u0637\u0628\u064a\u0629 \u0627\u0644\u062a\u0637\u0628\u064a\u0642\u064a\u0629')])),
                ('event', models.ForeignKey(blank=True, to='events.Event', null=True)),
                ('user', models.ForeignKey(verbose_name='\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u0640/\u0640\u0629', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='survey',
            name='category',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'COM', '\u0643\u0644\u064a\u0629 \u0627\u0644\u0637\u0628'), (b'COD', '\u062e\u064a\u0627\u0631\u0627\u062a'), (b'COAMS', '\u0627\u0644\u0639\u0644\u0648\u0645 \u0627\u0644\u0637\u0628\u064a\u0629 \u0627\u0644\u062a\u0637\u0628\u064a\u0642\u064a\u0629')]),
        ),
        migrations.AddField(
            model_name='survey',
            name='parent',
            field=models.ForeignKey(related_name='children', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='events.Survey', null=True, verbose_name=b'parent survey'),
        ),
    ]
