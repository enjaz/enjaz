# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0042_alahsa_deanship'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('is_english_name', models.BooleanField(default=False, verbose_name='\u0647\u0644 \u0627\u0633\u0645 \u0627\u0644\u062d\u062f\u062b \u0625\u0646\u062c\u0644\u064a\u0632\u064a')),
                ('code_name', models.CharField(default=b'', help_text='\u062d\u0631\u0648\u0641 \u0644\u0627\u062a\u064a\u0646\u064a\u0629 \u0635\u063a\u064a\u0631\u0629 \u0648\u0623\u0631\u0642\u0627\u0645', max_length=50, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0628\u0631\u0645\u062c\u064a', blank=True)),
                ('registration_opening_date', models.DateField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0641\u062a\u062d \u0627\u0644\u062a\u0633\u062c\u064a\u0644', blank=True)),
                ('registration_closing_date', models.DateField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0646\u062a\u0647\u0627\u0621 \u0627\u0644\u062a\u0633\u062c\u064a\u0644', blank=True)),
                ('start_date', models.DateField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0628\u062f\u0621')),
                ('end_date', models.DateField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0627\u0646\u062a\u0647\u0627\u0621')),
                ('url', models.CharField(max_length=255, blank=True)),
                ('priorities', models.PositiveSmallIntegerField(default=1)),
                ('organizing_club', models.ForeignKey(to='clubs.Club')),
            ],
        ),
        migrations.CreateModel(
            name='NonUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ar_first_name', models.CharField(default=b'', max_length=30, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0623\u0648\u0644', blank=True)),
                ('ar_middle_name', models.CharField(default=b'', max_length=30, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0623\u0648\u0633\u0637', blank=True)),
                ('ar_last_name', models.CharField(default=b'', max_length=30, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0623\u062e\u064a\u0631', blank=True)),
                ('en_first_name', models.CharField(max_length=30, verbose_name=b'First name')),
                ('en_middle_name', models.CharField(max_length=30, verbose_name=b'Middle name')),
                ('en_last_name', models.CharField(max_length=30, verbose_name=b'Last name')),
                ('gender', models.CharField(default=b'', max_length=1, verbose_name='\u0627\u0644\u062c\u0646\u0633', choices=[(b'F', '\u0637\u0627\u0644\u0628\u0629'), (b'M', '\u0637\u0627\u0644\u0628')])),
                ('email', models.EmailField(max_length=254, verbose_name='\u0627\u0644\u0628\u0631\u064a\u062f \u0627\u0644\u0625\u0644\u0643\u062a\u0631\u0648\u0646\u064a')),
                ('mobile_number', models.CharField(max_length=20, verbose_name='\u0631\u0642\u0645 \u0627\u0644\u062c\u0648\u0627\u0644')),
                ('university', models.CharField(max_length=255, verbose_name='\u0627\u0644\u062c\u0627\u0645\u0639\u0629')),
                ('college', models.CharField(max_length=255, verbose_name='\u0627\u0644\u0643\u0644\u064a\u0629')),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False, verbose_name='\u0645\u062d\u0630\u0648\u0641\u061f')),
                ('confirmation_sent', models.BooleanField(default=False, verbose_name='\u0623\u0631\u0633\u0644\u062a \u0631\u0633\u0627\u0644\u0629 \u0627\u0644\u062a\u0623\u0643\u064a\u062f\u061f')),
                ('reminder_sent', models.BooleanField(default=False, verbose_name='\u0623\u0631\u0633\u0644\u062a \u0631\u0633\u0627\u0644\u0629 \u0627\u0644\u062a\u0630\u0643\u064a\u0631\u061f')),
                ('certificate_sent', models.BooleanField(default=False, verbose_name='\u0623\u0631\u0633\u0644\u062a \u0627\u0644\u0634\u0647\u0627\u062f\u0629\u061f')),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('limit', models.PositiveSmallIntegerField(default=None, null=True, blank=True)),
                ('time_slot', models.PositiveSmallIntegerField(default=None, null=True, blank=True)),
                ('vma_id', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('vma_time_code', models.PositiveSmallIntegerField(default=None, null=True, blank=True)),
                ('code_name', models.CharField(default=b'', help_text='\u062d\u0631\u0648\u0641 \u0644\u0627\u062a\u064a\u0646\u064a\u0629 \u0635\u063a\u064a\u0631\u0629 \u0648\u0623\u0631\u0642\u0627\u0645', max_length=50, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0628\u0631\u0645\u062c\u064a', blank=True)),
                ('gender', models.CharField(default=b'', max_length=1, blank=True, choices=[(b'', '\u0627\u0644\u062c\u0645\u064a\u0639'), (b'F', '\u0637\u0627\u0644\u0628\u0627\u062a'), (b'M', '\u0637\u0644\u0627\u0628')])),
                ('location', models.CharField(default=b'', max_length=200, verbose_name='\u0627\u0644\u0645\u0643\u0627\u0646', blank=True)),
                ('date', models.DateField(null=True, verbose_name='\u0627\u0644\u062a\u0627\u0631\u064a\u062e')),
                ('start_time', models.TimeField(default=None, null=True, verbose_name='\u0648\u0642\u062a \u0627\u0644\u0628\u062f\u0627\u064a\u0629', blank=True)),
                ('end_time', models.TimeField(default=None, null=True, verbose_name='\u0648\u0642\u062a \u0627\u0644\u0646\u0647\u0627\u064a\u0629', blank=True)),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
                ('for_onsite_registration', models.BooleanField(default=False, verbose_name='\u0645\u062a\u0627\u062d \u0627\u0644\u062a\u0633\u062c\u064a\u0644 \u0641\u064a \u064a\u0648\u0645 \u0627\u0644\u062d\u062f\u062b\u061f')),
                ('event', models.ForeignKey(to='events.Event')),
            ],
        ),
        migrations.AddField(
            model_name='registration',
            name='first_priority_sessions',
            field=models.ManyToManyField(related_name='first_priory_registrations', to='events.Session', blank=True),
        ),
        migrations.AddField(
            model_name='registration',
            name='moved_sessions',
            field=models.ManyToManyField(related_name='moved_registrations', to='events.Session', blank=True),
        ),
        migrations.AddField(
            model_name='registration',
            name='nonuser',
            field=models.ForeignKey(related_name='event_registrations', blank=True, to='events.NonUser', null=True),
        ),
        migrations.AddField(
            model_name='registration',
            name='second_priority_sessions',
            field=models.ManyToManyField(related_name='second_priory_registrations', to='events.Session', blank=True),
        ),
        migrations.AddField(
            model_name='registration',
            name='user',
            field=models.ForeignKey(related_name='event_registrations', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
