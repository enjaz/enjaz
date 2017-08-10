# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clubs', '0052_presidencies_can_assess'),
        ('core', '0012_studentclubyear_bookexchange_open_date'),
        ('teams', '0004_rename_some_of_the_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ar_name', models.CharField(max_length=200, verbose_name='\u0627\u0644\u0627\u0633\u0645')),
                ('en_name', models.CharField(max_length=200, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0625\u0646\u062c\u0644\u064a\u0632\u064a')),
                ('code_name', models.CharField(max_length=200, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0628\u0631\u0645\u062c\u064a')),
                ('email', models.EmailField(max_length=254, verbose_name='\u0627\u0644\u0628\u0631\u064a\u062f \u0627\u0644\u0625\u0644\u0643\u062a\u0631\u0648\u0646\u064a')),
                ('city', models.CharField(max_length=20, verbose_name='\u0627\u0644\u0645\u062f\u064a\u0646\u0629', choices=[('\u0627\u0644\u0631\u064a\u0627\u0636', '\u0627\u0644\u0631\u064a\u0627\u0636'), ('\u062c\u062f\u0629', '\u062c\u062f\u0629'), ('\u0627\u0644\u0623\u062d\u0633\u0627\u0621', '\u0627\u0644\u0623\u062d\u0633\u0627\u0621')])),
                ('gender', models.CharField(default=b'', max_length=1, verbose_name='\u0627\u0644\u062c\u0646\u0633', blank=True, choices=[(b'F', '\u0637\u0627\u0644\u0628\u0627\u062a'), (b'M', '\u0637\u0644\u0627\u0628')])),
                ('category', models.CharField(max_length=2, verbose_name='\u0646\u0648\u0639 \u0627\u0644\u0641\u0631\u064a\u0642', choices=[(b'CC', b'\xd9\x86\xd8\xa7\xd8\xaf\xd9\x8a \xd9\x83\xd9\x84\xd9\x8a\xd8\xa9'), (b'SC', b'\xd9\x86\xd8\xa7\xd8\xaf\xd9\x8a \xd9\x85\xd8\xaa\xd8\xae\xd8\xb5\xd8\xb5'), (b'I', b'\xd9\x85\xd8\xa8\xd8\xa7\xd8\xaf\xd8\xb1\xd8\xa9'), (b'P', b'\xd8\xa8\xd8\xb1\xd9\x86\xd8\xa7\xd9\x85\xd8\xac \xd8\xb9\xd8\xa7\xd9\x85'), (b'CD', b'\xd8\xb9\xd9\x85\xd8\xa7\xd8\xaf\xd8\xa9 \xd9\x83\xd9\x84\xd9\x8a\xd8\xa9'), (b'SA', b'\xd8\xb9\xd9\x85\xd8\xa7\xd8\xaf\xd8\xa9 \xd8\xb4\xd8\xa4\xd9\x88\xd9\x86 \xd8\xa7\xd9\x84\xd8\xb7\xd9\x84\xd8\xa7\xd8\xa8'), (b'P', b'\xd8\xb1\xd8\xa6\xd8\xa7\xd8\xb3\xd8\xa9 \xd9\x86\xd8\xa7\xd8\xaf\xd9\x8a \xd8\xa7\xd9\x84\xd8\xb7\xd9\x84\xd8\xa7\xd8\xa8')])),
                ('is_visible', models.BooleanField(default=True, verbose_name='\u0645\u0631\u0626\u064a\u061f')),
                ('logo', models.ImageField(null=True, upload_to=b'teams/logos/', blank=True)),
                ('description', models.TextField(verbose_name='\u0627\u0644\u0648\u0635\u0641', blank=True)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='clubs.College', null=True, verbose_name='\u0627\u0644\u0643\u0644\u064a\u0629')),
                ('leader', models.ForeignKey(related_name='teams_leader', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u0646\u0633\u0642', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('members', models.ManyToManyField(related_name='teams', verbose_name='\u0627\u0644\u0623\u0639\u0636\u0627\u0621', to=settings.AUTH_USER_MODEL, blank=True)),
                ('parent', models.ForeignKey(related_name='children', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='teams.Team', null=True, verbose_name='\u0627\u0644\u0646\u0627\u062f\u064a \u0627\u0644\u0623\u0628')),
                ('year', models.ForeignKey(related_name='teams_of_year', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='core.StudentClubYear', null=True, verbose_name='\u0627\u0644\u0633\u0646\u0629')),
            ],
            options={
                'verbose_name': '\u0627\u0644\u0641\u0631\u064a\u0642',
                'verbose_name_plural': '\u0627\u0644\u0641\u0650\u0631\u0642',
            },
        ),
        migrations.RemoveField(
            model_name='teams',
            name='college',
        ),
        migrations.RemoveField(
            model_name='teams',
            name='leader',
        ),
        migrations.RemoveField(
            model_name='teams',
            name='members',
        ),
        migrations.RemoveField(
            model_name='teams',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='teams',
            name='year',
        ),
        migrations.DeleteModel(
            name='Teams',
        ),
    ]
