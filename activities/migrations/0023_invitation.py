# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activities', '0022_depository'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=100, verbose_name='\u0627\u0644\u0627\u0633\u0645')),
                ('background', models.ImageField(null=True, upload_to=b'invitations/backgrounds/', blank=True)),
                ('logo', models.ImageField(null=True, upload_to=b'invitations/backgrounds/', blank=True)),
                ('short_description', models.TextField(verbose_name='\u0648\u0635\u0641 \u0642\u0635\u064a\u0631')),
                ('full_description', models.TextField(verbose_name='\u0648\u0635\u0641 \u0642\u0635\u064a\u0631')),
                ('hashtag', models.CharField(default=b'', help_text=b'\xd8\xa8\xd8\xaf\xd9\x88\xd9\x86 #', max_length=20, verbose_name='\u0647\u0627\u0634\u062a\u0627\u063a', blank=True)),
                ('publication_date', models.DateTimeField(verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0646\u0634\u0631', blank=True)),
                ('location', models.CharField(default=b'', max_length=200, verbose_name='\u0627\u0644\u0645\u0643\u0627\u0646')),
                ('date', models.DateField(verbose_name='\u0627\u0644\u062a\u0627\u0631\u064a\u062e')),
                ('start_time', models.TimeField(verbose_name='\u0648\u0642\u062a \u0627\u0644\u0628\u062f\u0627\u064a\u0629')),
                ('end_time', models.TimeField(verbose_name='\u0648\u0642\u062a \u0627\u0644\u0646\u0647\u0627\u064a\u0629')),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('edit_date', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0639\u062f\u064a\u0644')),
                ('activity', models.ForeignKey(blank=True, to='activities.Activity', null=True)),
                ('students', models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
    ]
