# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('approvals', '0008_auto_20170913_2049'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityRequestComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('thread_id', models.PositiveIntegerField()),
                ('text', models.TextField(verbose_name='\u0627\u0644\u0646\u0635')),
                ('submission_datetime', models.DateTimeField(auto_now_add=True, verbose_name='\u0627\u0644\u062a\u0627\u0631\u064a\u062e \u0648 \u0627\u0644\u0648\u0642\u062a')),
                ('author', models.ForeignKey(related_name='activity_request_comments', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u0639\u0644\u0651\u0642', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': '\u062a\u0639\u0644\u064a\u0642',
                'verbose_name_plural': '\u062a\u0639\u0644\u064a\u0642\u0627\u062a',
            },
        ),
    ]
