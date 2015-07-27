# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activities', '0009_optional_gender_assignee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=200, verbose_name='\u0627\u0644\u0648\u0635\u0641')),
                ('preview', models.FileField(upload_to=b'media/activity_attachment_previews/', verbose_name='\u0645\u0639\u0627\u064a\u0646\u0629')),
                ('document', models.FileField(upload_to=b'media/activity_attachments/', verbose_name='\u0627\u0644\u0645\u0633\u062a\u0646\u062f')),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('activity', models.ForeignKey(to='activities.Activity')),
                ('submitter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='review',
            name='attachment_notes',
            field=models.TextField(verbose_name='\u0645\u0644\u0627\u062d\u0638\u0627\u062a \u0639\u0644\u0649 \u0627\u0644\u0645\u0633\u062a\u0646\u062f\u0627\u062a \u0627\u0644\u0645\u0631\u0641\u0642\u0629', blank=True),
        ),
    ]
