# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0028_allow_blank_organizers'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(default=b'', blank=True)),
                ('background', models.ImageField(null=True, upload_to=b'session_group/backgrounds/', blank=True)),
                ('code_name', models.CharField(default=b'', help_text='\u062d\u0631\u0648\u0641 \u0644\u0627\u062a\u064a\u0646\u064a\u0629 \u0635\u063a\u064a\u0631\u0629 \u0648\u0623\u0631\u0642\u0627\u0645', max_length=50, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0628\u0631\u0645\u062c\u064a', blank=True)),
                ('is_limited_to_one', models.BooleanField(default=False, verbose_name='\u0647\u0644 \u0627\u0644\u062a\u0633\u062c\u064a\u0644 \u0645\u0642\u062a\u0635\u0631 \u0639\u0644\u0649 \u062c\u0644\u0633\u0629 \u0648\u0627\u062d\u062f\u0629\u061f')),
                ('event', models.ForeignKey(blank=True, to='events.Event', null=True)),
                ('sessions', models.ManyToManyField(to='events.Session', blank=True)),
            ],
        ),
    ]
