# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0021_abstract_previous_participation_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionRegistration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('is_approved', models.NullBooleanField(default=None, verbose_name='\u0627\u0644\u062d\u0627\u0644\u0629', choices=[(True, '\u0645\u0639\u062a\u0645\u062f'), (False, '\u0645\u0631\u0641\u0648\u0636'), (None, '\u0645\u0639\u0644\u0642')])),
                ('is_deleted', models.BooleanField(default=False, verbose_name='\u0645\u062d\u0630\u0648\u0641\u061f')),
                ('reminder_sent', models.BooleanField(default=False, verbose_name='\u0623\u0631\u0633\u0644\u062a \u0631\u0633\u0627\u0644\u0629 \u0627\u0644\u062a\u0630\u0643\u064a\u0631\u061f')),
                ('certificate_sent', models.BooleanField(default=False, verbose_name='\u0623\u0631\u0633\u0644\u062a \u0627\u0644\u0634\u0647\u0627\u062f\u0629\u061f')),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(to='events.Event')),
            ],
        ),
        migrations.AddField(
            model_name='session',
            name='acceptance_method',
            field=models.CharField(default=b'', max_length=1, verbose_name=b'acceptance_method', choices=[(b'F', b'First ComeFirst Serve'), (b'M', b'Manual')]),
        ),
        migrations.AddField(
            model_name='session',
            name='description',
            field=models.TextField(default=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='event',
            field=models.ForeignKey(blank=True, to='events.Event', null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='time_slot',
            field=models.ForeignKey(default=b'', to='events.TimeSlot', null=True),
        ),
        migrations.AddField(
            model_name='sessionregistration',
            name='session',
            field=models.ForeignKey(to='events.Session'),
        ),
        migrations.AddField(
            model_name='sessionregistration',
            name='user',
            field=models.ForeignKey(related_name='session_registrations', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
