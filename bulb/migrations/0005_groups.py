# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_studentclubyear_niqati_closure_date'),
        ('bulb', '0004_initial_balance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.FileField(upload_to=b'bulb/groups/', verbose_name='\u0627\u0644\u0635\u0648\u0631\u0629')),
                ('name', models.CharField(max_length=200, verbose_name='\u0627\u0644\u0627\u0633\u0645')),
                ('description', models.TextField(verbose_name='\u0648\u0635\u0641')),
                ('gender', models.CharField(default=b'', max_length=1, verbose_name='\u0627\u0644\u0645\u062c\u0645\u0648\u0639\u0629 \u0645\u0648\u062c\u0651\u0647\u0629 \u0625\u0644\u0649', blank=True, choices=[(b'', '\u0627\u0644\u062c\u0645\u064a\u0639'), (b'F', '\u0627\u0644\u0637\u0627\u0644\u0628\u0627\u062a'), (b'M', '\u0627\u0644\u0637\u0644\u0627\u0628')])),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('modifiation_date', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0639\u062f\u064a\u0644')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='\u0645\u062d\u0630\u0648\u0641\u0629\u061f')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u062a\u0635\u0646\u064a\u0641\u0627\u062a', to='bulb.Category', null=True)),
                ('coordinator', models.ForeignKey(related_name='reading_group_coordination', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u0646\u0633\u0642', to=settings.AUTH_USER_MODEL, null=True)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='core.StudentClubYear', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='\u0645\u0641\u0639\u0644\u0629\u061f')),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('modifiation_date', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0639\u062f\u064a\u0644')),
                ('group', models.ForeignKey(verbose_name='\u0627\u0644\u0645\u062c\u0645\u0648\u0639\u0629', to='bulb.Group')),
                ('user', models.ForeignKey(related_name='reading_group_memberships', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u0646\u0633\u0642', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(verbose_name='\u0645\u062c\u0631\u064a\u0627\u062a \u0627\u0644\u062c\u0644\u0633\u0629')),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('attendees', models.ManyToManyField(related_name='reading_group_attendance', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='\u0639\u0646\u0648\u0627\u0646 \u0627\u0644\u062c\u0644\u0633\u0629')),
                ('agenda', models.TextField(verbose_name='\u0645\u062d\u0627\u0648\u0631 \u0627\u0644\u062c\u0644\u0633\u0629')),
                ('location', models.CharField(max_length=200, verbose_name='\u0627\u0644\u0645\u0643\u0627\u0646')),
                ('date', models.DateField(verbose_name='\u0627\u0644\u062a\u0627\u0631\u064a\u062e')),
                ('start_time', models.TimeField(verbose_name='\u0648\u0642\u062a \u0627\u0644\u0628\u062f\u0627\u064a\u0629')),
                ('end_time', models.TimeField(verbose_name='\u0648\u0642\u062a \u0627\u0644\u0646\u0647\u0627\u064a\u0629')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='\u0645\u062d\u0630\u0648\u0641\u0629\u061f')),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u062c\u0645\u0648\u0639\u0629', to='bulb.Group', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='report',
            name='session',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u062c\u0644\u0633\u0629', to='bulb.Session'),
        ),
    ]
