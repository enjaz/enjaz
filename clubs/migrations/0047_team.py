# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0009_tweet_failed_trials'),
        ('clubs', '0046_add_jeddah_ams_deanship'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='\u0627\u0644\u0627\u0633\u0645')),
                ('code_name', models.CharField(max_length=200, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0628\u0631\u0645\u062c\u064a')),
                ('email', models.EmailField(max_length=254, verbose_name='\u0627\u0644\u0628\u0631\u064a\u062f \u0627\u0644\u0625\u0644\u0643\u062a\u0631\u0648\u0646\u064a', blank=True)),
                ('city', models.CharField(default=b'', max_length=1, verbose_name='\u0627\u0644\u0645\u062f\u064a\u0646\u0629', blank=True, choices=[(b'R', '\u0627\u0644\u0631\u064a\u0627\u0636'), (b'J', '\u062c\u062f\u0629'), (b'A', '\u0627\u0644\u0623\u062d\u0633\u0627\u0621')])),
                ('gender', models.CharField(default=b'', max_length=1, verbose_name='\u0627\u0644\u062c\u0646\u062f\u0631', blank=True, choices=[(b'F', '\u0637\u0627\u0644\u0628\u0627\u062a'), (b'M', '\u0637\u0644\u0627\u0628')])),
                ('club', models.ForeignKey(verbose_name='\u0627\u0644\u0646\u0627\u062f\u064a \u0627\u0644\u0645\u062a\u0635\u0644', blank=True, to='clubs.Club', null=True)),
                ('coordinator', models.ForeignKey(verbose_name='\u0627\u0644\u0645\u0646\u0633\u0642', blank=True, to=settings.AUTH_USER_MODEL, null=True, related_name="team_coordination")),
                ('members', models.ManyToManyField(related_name='team_memberships', verbose_name='\u0627\u0644\u0623\u0639\u0636\u0627\u0621', to=settings.AUTH_USER_MODEL, blank=True)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='core.StudentClubYear', null=True, verbose_name='\u0627\u0644\u0633\u0646\u0629')),
            ],
            options={
                'verbose_name': '\u0641\u0631\u064a\u0642',
                'verbose_name_plural': '\u0627\u0644\u0641\u0631\u0642',
            },
        ),
    ]
