# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0008_add_collection_method'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booth',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u0627\u0633\u0645 \u0627\u0644\u0631\u0643\u0646')),
                ('event', models.ForeignKey(verbose_name=b'\xd8\xa7\xd9\x84\xd8\xad\xd8\xaf\xd8\xab', to='events.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0635\u0648\u064a\u062a')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='\u0645\u062d\u0630\u0648\u0641\u061f')),
                ('booth', models.ForeignKey(verbose_name=b'\xd8\xa7\xd8\xb3\xd9\x85 \xd8\xa7\xd9\x84\xd8\xb1\xd9\x83\xd9\x86', to='events.Booth')),
                ('submitter', models.ForeignKey(related_name='event_booth_voter', verbose_name=b'\xd8\xa7\xd8\xb3\xd9\x85 \xd8\xa7\xd9\x84\xd9\x85\xd8\xb5\xd9\x88\xd8\xaa', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
