# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hpc', '0005_extend_max_lengths'),
    ]

    operations = [
        migrations.CreateModel(
            name='NonUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ar_name', models.CharField(max_length=255, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0639\u0631\u0628\u064a')),
                ('en_name', models.CharField(max_length=255, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0625\u0646\u062c\u0644\u064a\u0632\u064a')),
                ('email', models.EmailField(max_length=254)),
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
                ('nonuser', models.OneToOneField(related_name='hpc2016_registration', null=True, blank=True, to='hpc.NonUser')),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('limit', models.PositiveSmallIntegerField(default=None, null=True)),
                ('name', models.CharField(max_length=255)),
                ('time_slot', models.PositiveSmallIntegerField(default=None, null=True)),
                ('vma_id', models.PositiveSmallIntegerField()),
                ('gender', models.CharField(default=b'', max_length=1, choices=[(b'F', '\u0637\u0627\u0644\u0628\u0627\u062a'), (b'M', '\u0637\u0644\u0627\u0628')])),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='registration',
            name='sessions',
            field=models.ManyToManyField(to='hpc.Session', blank=True),
        ),
        migrations.AddField(
            model_name='registration',
            name='user',
            field=models.OneToOneField(related_name='hpc2016_registration', null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
