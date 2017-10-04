# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='\u0627\u0633\u0645 \u0627\u0644\u0646\u0634\u0627\u0637')),
                ('description', models.TextField(verbose_name='\u0648\u0635\u0641 \u0627\u0644\u0646\u0634\u0627\u0637')),
                ('public_description', models.TextField(help_text='\u0647\u0630\u0627 \u0647\u0648 \u0627\u0644\u0648\u0635\u0641 \u0627\u0644\u0630\u064a \u0633\u064a\u0639\u0631\u0636 \u0644\u0644\u0637\u0644\u0627\u0628', verbose_name='\u0627\u0644\u0648\u0635\u0641 \u0627\u0644\u0625\u0639\u0644\u0627\u0645\u064a')),
                ('goals', models.TextField(verbose_name='\u0645\u0627 \u0623\u0647\u062f\u0627\u0641 \u0647\u0630\u0627 \u0627\u0644\u0646\u0634\u0627\u0637\u060c \u0648\u0643\u064a\u0641 \u064a\u062e\u062f\u0645 \u0627\u0644\u0645\u062c\u062a\u0645\u0639 \u0648\u0627\u0644\u0635\u0627\u0644\u062d \u0627\u0644\u0639\u0627\u0645\u061f')),
                ('requirements', models.TextField(verbose_name='\u0645\u062a\u0637\u0644\u0628\u0627\u062a \u0627\u0644\u0646\u0634\u0627\u0637 \u0627\u0644\u0623\u062e\u0631\u0649', blank=True)),
                ('is_deleted', models.BooleanField(default=False, verbose_name='\u0645\u062d\u0630\u0648\u0641\u061f')),
                ('inside_collaborators', models.TextField(verbose_name='\u0627\u0644\u0645\u062a\u0639\u0627\u0648\u0646\u0648\u0646 \u0645\u0646 \u062f\u0627\u062e\u0644 \u0627\u0644\u062c\u0627\u0645\u0639\u0629', blank=True)),
                ('outside_collaborators', models.TextField(verbose_name='\u0627\u0644\u0645\u062a\u0639\u0627\u0648\u0646\u0648\u0646 \u0645\u0646 \u062e\u0627\u0631\u062c \u0627\u0644\u062c\u0627\u0645\u0639\u0629', blank=True)),
                ('participants', models.IntegerField(help_text='\u0627\u0644\u0639\u062f\u062f \u0627\u0644\u0645\u062a\u0648\u0642\u0639 \u0644\u0644\u0645\u0633\u062a\u0641\u064a\u062f\u064a\u0646 \u0645\u0646 \u0627\u0644\u0646\u0634\u0627\u0637', verbose_name='\u0639\u062f\u062f \u0627\u0644\u0645\u0634\u0627\u0631\u0643\u064a\u0646')),
                ('organizers', models.IntegerField(help_text='\u0639\u062f\u062f \u0627\u0644\u0637\u0644\u0627\u0628 \u0627\u0644\u0630\u064a\u0646 \u0633\u064a\u0646\u0638\u0645\u0648\u0646 \u0627\u0644\u0646\u0634\u0627\u0637', verbose_name='\u0639\u062f\u062f \u0627\u0644\u0645\u0646\u0638\u0645\u064a\u0646')),
                ('gender', models.CharField(default=b'', max_length=1, verbose_name='\u0627\u0644\u0646\u0634\u0627\u0637 \u0645\u0648\u062c\u0647 \u0644', blank=True, choices=[(b'', '\u0627\u0644\u062c\u0645\u064a\u0639'), (b'F', '\u0627\u0644\u0637\u0627\u0644\u0628\u0627\u062a'), (b'M', '\u0627\u0644\u0637\u0644\u0627\u0628')])),
                ('is_approved', models.NullBooleanField(verbose_name='\u0627\u0644\u062d\u0627\u0644\u0629', choices=[(True, '\u0645\u0639\u062a\u0645\u062f'), (False, '\u0645\u0631\u0641\u0648\u0636'), (None, '\u0645\u0639\u0644\u0642')])),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submission_date', models.DateField(verbose_name=b'Event date')),
                ('start_time', models.TimeField(verbose_name=b'Starting time')),
                ('end_time', models.TimeField(verbose_name=b'Ending time')),
                ('name', models.CharField(max_length=200, verbose_name=b'Event name')),
                ('location', models.CharField(max_length=128, verbose_name=b'Event location')),
                ('short_description', models.CharField(max_length=128, verbose_name=b'Short description of the event')),
                ('activity', models.ForeignKey(to='activities2.Activity')),
            ],
        ),
    ]
