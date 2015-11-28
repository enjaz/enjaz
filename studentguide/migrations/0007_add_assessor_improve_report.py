# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('studentguide', '0006_tag_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='text',
        ),
        migrations.AddField(
            model_name='guideprofile',
            name='assessor',
            field=models.ForeignKey(related_name='studentguide_assessments', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u0627\u0644\u0645\u064f\u0642\u064a\u0651\u0645'),
        ),
        migrations.AddField(
            model_name='report',
            name='issues_faced',
            field=models.TextField(default=b'', help_text='\u0627\u062e\u062a\u064a\u0627\u0631\u064a', verbose_name='\u0647\u0644 \u0645\u0646 \u0635\u0639\u0648\u0628\u0627\u062a \u0641\u064a \u0639\u0642\u062f \u0627\u0644\u062c\u0644\u0633\u0629\u061f', blank=True),
        ),
        migrations.AddField(
            model_name='report',
            name='means_of_communication',
            field=models.CharField(default='', max_length=200, verbose_name='\u0648\u0633\u064a\u0644\u0629 \u0627\u0644\u062a\u0648\u0627\u0635\u0644 \u0627\u0644\u0645\u0639\u062a\u0645\u062f\u0629 \u0645\u0639 \u0627\u0644\u0637\u0644\u0628\u0629 \u0627\u0644\u0645\u0633\u062a\u0641\u064a\u062f\u064a\u0646'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='next_session_date',
            field=models.DateField(help_text='\u0627\u062e\u062a\u064a\u0627\u0631\u064a', null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062c\u0644\u0633\u0629 \u0627\u0644\u0642\u0627\u062f\u0645\u0629', blank=True),
        ),
        migrations.AddField(
            model_name='report',
            name='other_comments',
            field=models.TextField(default='', verbose_name='\u0645\u0644\u0627\u062d\u0638\u0627\u062a \u0623\u062e\u0631\u0649'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='plans_suggested',
            field=models.TextField(default='', verbose_name='\u0627\u0644\u062e\u0637\u0637 \u0648\u0627\u0644\u062d\u0644\u0648\u0644 \u0627\u0644\u062a\u064a \u0648\u064f\u0636\u0639\u062a'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='points_discussed',
            field=models.TextField(default='', verbose_name='\u0627\u0644\u0645\u0634\u0643\u0644\u0627\u062a \u0648\u0627\u0644\u0642\u0636\u0627\u064a\u0627 \u0627\u0644\u062a\u064a \u0646\u0648\u0642\u0634\u062a'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='session_date',
            field=models.DateField(default=datetime.datetime(2015, 11, 28, 20, 29, 16, 171342, tzinfo=utc), verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062c\u0644\u0633\u0629'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='session_duration',
            field=models.CharField(default='', max_length=200, verbose_name='\u0645\u062f\u0629 \u0627\u0644\u062c\u0644\u0633\u0629'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='session_location',
            field=models.CharField(default='', max_length=200, verbose_name='\u0645\u0643\u0627\u0646 \u0627\u0644\u062c\u0644\u0633\u0629'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='feedback',
            name='text',
            field=models.TextField(verbose_name='\u0645\u0644\u0627\u062d\u0638\u062a\u0643'),
        ),
    ]
