# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import easy_thumbnails.fields
import django.db.models.deletion
from django.conf import settings
import userena.models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EnjazBaseProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ar_first_name', models.CharField(max_length=30, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0623\u0648\u0644')),
                ('ar_middle_name', models.CharField(max_length=30, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0623\u0648\u0633\u0637')),
                ('ar_last_name', models.CharField(max_length=30, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0623\u062e\u064a\u0631')),
                ('en_first_name', models.CharField(max_length=30, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0623\u0648\u0644')),
                ('en_middle_name', models.CharField(max_length=30, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0623\u0648\u0633\u0637')),
                ('en_last_name', models.CharField(max_length=30, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0623\u062e\u064a\u0631')),
                ('badge_number', models.IntegerField(null=True, verbose_name='\u0631\u0642\u0645 \u0627\u0644\u0628\u0637\u0627\u0642\u0629')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EnjazProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mugshot', easy_thumbnails.fields.ThumbnailerImageField(help_text='A personal image displayed in your profile.', upload_to=userena.models.upload_to_mugshot, verbose_name='mugshot', blank=True)),
                ('privacy', models.CharField(default=b'registered', help_text='Designates who can view your profile.', max_length=15, verbose_name='privacy', choices=[(b'open', 'Open'), (b'registered', 'Registered'), (b'closed', 'Closed')])),
                ('user', models.OneToOneField(related_name='enjaz_profile', verbose_name='\u0645\u0633\u062a\u062e\u062f\u0645', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'permissions': (('view_profile', 'Can view profile'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NonStudentProfile',
            fields=[
                ('enjazbaseprofile_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='accounts.EnjazBaseProfile')),
                ('mobile_number', models.CharField(max_length=20, verbose_name='\u0631\u0642\u0645 \u0627\u0644\u062c\u0648\u0627\u0644 (\u0627\u062e\u062a\u064a\u0627\u0631\u064a)', blank=True)),
                ('job_description', models.CharField(max_length=50, verbose_name='\u0627\u0644\u0645\u0633\u0645\u0649 \u0627\u0644\u0648\u0638\u064a\u0641\u064a')),
                ('user', models.OneToOneField(related_name='nonstudent_profile', verbose_name='\u0645\u0633\u062a\u062e\u062f\u0645', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u0645\u0644\u0641 \u0645\u0633\u062a\u062e\u062f\u0645 \u0622\u062e\u0631',
                'verbose_name_plural': '\u0645\u0644\u0641\u0627\u062a \u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u064a\u0646 \u0627\u0644\u0622\u062e\u0631\u064a\u0646',
            },
            bases=('accounts.enjazbaseprofile',),
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('enjazbaseprofile_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='accounts.EnjazBaseProfile')),
                ('student_id', models.IntegerField(null=True, verbose_name='\u0627\u0644\u0631\u0642\u0645 \u0627\u0644\u062c\u0627\u0645\u0639\u064a', blank=True)),
                ('mobile_number', models.CharField(max_length=20, verbose_name='\u0631\u0642\u0645 \u0627\u0644\u062c\u0648\u0627\u0644')),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0643\u0644\u064a\u0629', to='clubs.College', null=True)),
                ('user', models.OneToOneField(related_name='student_profile', verbose_name='\u0645\u0633\u062a\u062e\u062f\u0645', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u0645\u0644\u0641 \u0637\u0627\u0644\u0628',
                'verbose_name_plural': '\u0645\u0644\u0641\u0627\u062a \u0627\u0644\u0637\u0644\u0627\u0628',
            },
            bases=('accounts.enjazbaseprofile',),
        ),
    ]
