# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clubs', '0009_more_sections_and_club_gender'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommonProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_student', models.BooleanField(default=True, verbose_name='\u0637\u0627\u0644\u0628\u061f')),
                ('ar_first_name', models.CharField(max_length=30, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0623\u0648\u0644')),
                ('ar_middle_name', models.CharField(max_length=30, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0623\u0648\u0633\u0637')),
                ('ar_last_name', models.CharField(max_length=30, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0623\u062e\u064a\u0631')),
                ('en_first_name', models.CharField(max_length=30, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0623\u0648\u0644')),
                ('en_middle_name', models.CharField(max_length=30, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0623\u0648\u0633\u0637')),
                ('en_last_name', models.CharField(max_length=30, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0623\u062e\u064a\u0631')),
                ('badge_number', models.IntegerField(null=True, verbose_name='\u0631\u0642\u0645 \u0627\u0644\u0628\u0637\u0627\u0642\u0629')),
                ('mobile_number', models.CharField(max_length=20, verbose_name='\u0631\u0642\u0645 \u0627\u0644\u062c\u0648\u0627\u0644')),
                ('city', models.CharField(default=b'R', max_length=1, verbose_name='\u0627\u0644\u0645\u062f\u064a\u0646\u0629', choices=[(b'R', '\u0627\u0644\u0631\u064a\u0627\u0636'), (b'J', '\u062c\u062f\u0629'), (b'A', '\u0627\u0644\u0623\u062d\u0633\u0627\u0621')])),
                ('student_id', models.IntegerField(null=True, verbose_name='\u0627\u0644\u0631\u0642\u0645 \u0627\u0644\u062c\u0627\u0645\u0639\u064a', blank=True)),
                ('job_description', models.CharField(max_length=50, verbose_name='\u0627\u0644\u0645\u0633\u0645\u0649 \u0627\u0644\u0648\u0638\u064a\u0641\u064a', blank=True)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0643\u0644\u064a\u0629', blank=True, to='clubs.College', null=True)),
                ('user', models.OneToOneField(related_name='common_profile', verbose_name='\u0645\u0633\u062a\u062e\u062f\u0645', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
