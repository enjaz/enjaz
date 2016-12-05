# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0027_invitation_maximum_registrants'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bulb', '0025_pages'),
    ]

    operations = [
        migrations.CreateModel(
            name='CulturalProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('author', models.CharField(max_length=200, verbose_name='\u0627\u0644\u0645\u0624\u0644\u0641\u0640/\u0640\u0629')),
                ('body', models.TextField(verbose_name='\u0627\u0644\u062c\u0633\u0645')),
                ('readathon', models.ForeignKey(verbose_name='\u0627\u0644\u0631\u064a\u062f\u064a\u062b\u0648\u0646', to='bulb.Readathon')),
            ],
        ),
        migrations.CreateModel(
            name='Debate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('statement', models.CharField(max_length=200, verbose_name='\u0639\u0628\u0627\u0631\u0629 \u0627\u0644\u0645\u0646\u0627\u0638\u0631\u0629')),
                ('description', models.TextField(verbose_name='\u0627\u0644\u0648\u0635\u0641')),
                ('comment_closure_date', models.DateTimeField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0625\u0642\u0641\u0627\u0644 \u0627\u0644\u062a\u0639\u0644\u064a\u0642\u0627\u062a', blank=True)),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('invitation', models.ForeignKey(verbose_name='\u0627\u0644\u062f\u0639\u0648\u0629', blank=True, to='activities.Invitation', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DebateComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_for', models.BooleanField(verbose_name='\u0645\u0624\u064a\u062f\u061f')),
                ('title', models.CharField(max_length=200, verbose_name='\u0627\u0644\u0639\u0646\u0648\u0627\u0646')),
                ('body', models.TextField(verbose_name='\u0627\u0644\u062a\u0639\u0644\u064a\u0642')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='\u0645\u062d\u0630\u0648\u0641\u061f')),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('debate', models.ForeignKey(verbose_name='\u0627\u0644\u0645\u0646\u0627\u0638\u0631\u0629', to='bulb.Debate')),
                ('user', models.ForeignKey(verbose_name='\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u0640/\u0640\u0629', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
